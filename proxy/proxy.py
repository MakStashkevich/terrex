import socket
import threading
import sys
from typing import BinaryIO
from proxy.config import config
from terrex.packets.packet_ids import PacketIds
from proxy.parser import IncrementalParser

BUFFER_SIZE = 4096
SERVER_ADDR = ('t.makstashkevich.com', 7777) # 127.0.0.1
BIND_ADDR = ('127.0.0.1', 8888)

def toggle_cfg_tags(dir: str, tag: str, value: bool) -> str:
    with config.lock:
        if dir == "in":
            in_, out_ = True, False
        elif dir == "out":
            in_, out_ = False, True
        elif dir == "both":
            in_, out_ = True, True
        else:
            return "Invalid direction"

        if tag == "all":
            if in_:
                config.dbg_in_tags = [value] * 256
            if out_:
                config.dbg_out_tags = [value] * 256
            return "Success"

        try:
            t = int(tag)
            if 0 <= t < 256:
                if in_:
                    config.dbg_in_tags[t] = value
                if out_:
                    config.dbg_out_tags[t] = value
                return "Success"
            return "Tag out of range"
        except ValueError:
            return "Failed to parse tag number"

def user_input():
    print("Now handling user input. Type help for help")
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        argv = line.split()
        if not argv:
            continue
        cmd = argv[0]
        if cmd == "help":
            print("""
* help: show this message
* quit: stop processing stdin
* show <in|out|both> <all|TAG>: show the dbg repr of matching messages
* hide <in|out|both> <all|TAG>: hide the dbg repr of matching messages
* list: list all tags along with the name
* flush: flush network traffic writes to disk
* nosave: stop saving network traffic to disk
""")
            continue
        if cmd == "quit":
            sys.exit(0)
        if cmd in ("show", "hide"):
            if len(argv) != 3:
                print("Both dir and tag must be provided")
                continue
            dirr, tag = argv[1], argv[2]
            value = (cmd == "show")
            print(toggle_cfg_tags(dirr, tag, value))
        elif cmd == "list":
            print("Packet tags:")
            for pid in PacketIds:
                print(f"  {pid.value:3d} (0x{pid.value:02X}): {pid.name}")
        elif cmd == "flush":
            with config.lock:
                config.flush_traffic[0] = True
                config.flush_traffic[1] = True
        elif cmd == "nosave":
            with config.lock:
                if config.server_traffic:
                    config.server_traffic.close()
                    config.server_traffic = None
                if config.client_traffic:
                    config.client_traffic.close()
                    config.client_traffic = None
            print("Dropped open files")
        else:
            print(f"Could not understand \"{cmd}\". Type help for help")

def forward(direction: str, read_sock: socket.socket, write_sock: socket.socket, parser, traffic_file: BinaryIO | None, flush_idx: int, tags: list[bool]):
    buf = bytearray(BUFFER_SIZE)
    while True:
        n = read_sock.recv_into(buf)
        if n == 0:
            break
        data = bytes(buf[:n])
        with config.lock:
            parser.feed(data)
            while True:
                packet = parser.next()
                if packet is None:
                    break
                try:
                    if tags[packet.id]:
                        try:
                            pkt_name = str(PacketIds.from_id(packet.id))
                        except ValueError:
                            pkt_name = f"Unknown(0x{packet.id:02X})"
                        print(f"{direction}{'<' if direction == 'STC' else '>'} {packet.id} {pkt_name} {vars(packet)}")
                except Exception as e:
                    print(f"{direction}! bad packet: {e}")
            if traffic_file is not None:
                traffic_file.write(data)
                if config.flush_traffic[flush_idx]:
                    traffic_file.flush()
                    config.flush_traffic[flush_idx] = False
        try:
            write_sock.sendall(data)
        except:
            break
    print(f"{direction} task exited")
    read_sock.close()

def main():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"Binding socket to {BIND_ADDR}...")
    listener.bind(BIND_ADDR)
    listener.listen(1)
    print(f"Socket bound to {BIND_ADDR}. Accepting incoming client connection...")
    try:
        client_sock, client_addr = listener.accept()
    except KeyboardInterrupt:
        print("\nShutdown requested. Exiting cleanly.")
        listener.close()
        return
    listener.close()
    print(f"Accepted client {client_addr}!")
    print(f"Connecting to the server {SERVER_ADDR}...")
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect(SERVER_ADDR)
    print("Connected to the server!")
    print("Launching input thread (UIT)...")
    input_thread = threading.Thread(target=user_input, daemon=True)
    input_thread.start()
    print("Launching Server-to-Client task (STC)...")
    stc_thread = threading.Thread(
        target=forward,
        args=("STC", server_sock, client_sock, config.server_parser, config.server_traffic, 0, config.dbg_out_tags),
        daemon=True
    )
    stc_thread.start()
    print("Launching Client-to-Server task (CTS)...")
    cts_thread = threading.Thread(
        target=forward,
        args=("CTS", client_sock, server_sock, config.client_parser, config.client_traffic, 1, config.dbg_in_tags),
        daemon=True
    )
    cts_thread.start()
    try:
        stc_thread.join()
        cts_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down proxy gracefully...")

if __name__ == "__main__":
    main()
