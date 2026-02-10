import socket
import threading
import sys
import argparse
from datetime import datetime
from proxy.config import config
from terrex.packets.packet_ids import PacketIds
from terrex.packets.base import stringify_value
from proxy.parser import IncrementalParser

IGNORED_PACKET_IDS = [PacketIds.SEND_SECTION]

BUFFER_SIZE = 4096


def current_timestamp() -> str:
    return datetime.now().astimezone().isoformat(sep=" ", timespec="milliseconds")


def toggle_cfg_tags(dir: str, tag: str, value: bool) -> str:
    """Toggle debugging tags for packet logging.

    Args:
        dir: 'in' (CTS/client->server), 'out' (STC/server->client), 'both'.
        tag: 'all' or specific packet ID (0-255).
        value: True to show, False to hide.

    Returns:
        Status message.
    """
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
                config.dbg_in_tags[:] = [value] * 256
                print(f"Set in_tags (CTS) to {value}")
            if out_:
                config.dbg_out_tags[:] = [value] * 256
                print(f"Set out_tags (STC) to {value}")
            return "Success"

        try:
            t = int(tag)
            if 0 <= t < 256:
                old_in = config.dbg_in_tags[t] if in_ else None
                old_out = config.dbg_out_tags[t] if out_ else None
                if in_:
                    config.dbg_in_tags[t] = value
                if out_:
                    config.dbg_out_tags[t] = value
                print(
                    f"Tag {t}: in={old_in}->{value if in_ else old_in}, out={old_out}->{value if out_ else old_out}"
                )
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
            print(
                """
* help: show this message
* quit: stop processing stdin
* show <in|out|both> <all|TAG>: show the dbg repr of matching messages
* hide <in|out|both> <all|TAG>: hide the dbg repr of matching messages
* list: list all tags along with the name
* flush: flush network traffic writes to disk
* nosave: stop saving network traffic to disk
"""
            )
            continue
        if cmd == "quit":
            sys.exit(0)
        if cmd in ("show", "hide"):
            if len(argv) != 3:
                print("Both dir and tag must be provided")
                continue
            dirr, tag = argv[1], argv[2]
            value = cmd == "show"
            print(toggle_cfg_tags(dirr, tag, value))
        elif cmd == "list":
            print("Packet tags:")
            for pid in PacketIds:
                print(f"  {pid.value:3d} (0x{pid.value:02X}): {pid.name}")
        elif cmd == "flush":
            with config.lock:
                config.flush_bin[0] = True
                config.flush_bin[1] = True
                config.flush_txt[0] = True
                config.flush_txt[1] = True
                config.flush_both_txt = True
            print("Flush for all traffic to files enabled")
        elif cmd == "nosave":
            with config.lock:
                if config.server_traffic_bin:
                    config.server_traffic_bin.close()
                    config.server_traffic_bin = None
                if config.client_traffic_bin:
                    config.client_traffic_bin.close()
                    config.client_traffic_bin = None
                if config.server_traffic_txt:
                    config.server_traffic_txt.close()
                    config.server_traffic_txt = None
                if config.client_traffic_txt:
                    config.client_traffic_txt.close()
                    config.client_traffic_txt = None
                if config.both_traffic_txt:
                    config.both_traffic_txt.close()
                    config.both_traffic_txt = None
        else:
            print(f'Could not understand "{cmd}". Type help for help')


def forward(
    direction: str,
    read_sock: socket.socket,
    write_sock: socket.socket,
    parser: IncrementalParser,
    tags: list[bool],
):
    """Forward raw traffic from read_sock to write_sock while parsing packets for logging.

    - Receives raw data chunks from read_sock.
    - Feeds data to parser to extract complete packets.
    - Logs parsed packets if their ID is tagged for debugging.
    - Writes raw traffic to file if enabled.
    - Forwards raw data unchanged to write_sock.

    Args:
        direction: 'STC' or 'CTS' for logging prefix.
        read_sock: Socket to read raw traffic from.
        write_sock: Socket to forward raw traffic to.
        parser: Incremental parser for packet extraction.
        traffic_file: Optional file to log raw traffic.
        flush_idx: Index for flush flag (0 for STC, 1 for CTS).
        tags: List of booleans indicating which packet IDs to log.
    """
    buf = bytearray(BUFFER_SIZE)
    while True:
        try:
            n = read_sock.recv_into(buf)
        except:
            break
        if n == 0:
            break
        data = bytes(buf[:n])

        # if direction == "CTS":
        #     from proxy.middleware import client_packet_middleware
        #     data = client_packet_middleware(data)

        # Determine traffic files
        if direction == "STC":
            traffic_bin = config.server_traffic_bin
            traffic_txt = config.server_traffic_txt
            flush_bin_idx = 0
            flush_txt_idx = 0
        else:  # CTS
            traffic_bin = config.client_traffic_bin
            traffic_txt = config.client_traffic_txt
            flush_bin_idx = 1
            flush_txt_idx = 1

        # Thread-safe packet parsing and logging
        with config.lock:
            parser.feed(data)
            while True:
                packet = parser.next()
                if packet is None:
                    break
                try:
                    # Get packet name
                    try:
                        pkt_name = str(PacketIds.from_id(packet.id))
                    except ValueError:
                        pkt_name = f"Unknown(0x{packet.id:02X})"

                    timestamp = current_timestamp()
                    log_payload = stringify_value(vars(packet))

                    if packet.id in IGNORED_PACKET_IDS:
                        continue

                    if tags[packet.id]:
                        print(
                            f"{direction}{'<' if direction == 'STC' else '>'} {packet.id} {pkt_name} {log_payload}"
                        )

                    # Log to txt if enabled (all packets)
                    if traffic_txt is not None:
                        traffic_txt.write(
                            f"[{timestamp}] ---0x{packet.id:02X} {pkt_name} ---\n"
                        )
                        traffic_txt.write(f"{log_payload}\n\n")
                        if config.flush_txt[flush_txt_idx]:
                            traffic_txt.flush()

                    # Log to shared both-traffic file
                    if config.both_traffic_txt is not None:
                        config.both_traffic_txt.write(
                            f"{direction} ---0x{packet.id:02X} {pkt_name} ---\n"
                        )
                        config.both_traffic_txt.write(f"{log_payload}\n\n")
                        if config.flush_both_txt:
                            config.both_traffic_txt.flush()
                except Exception as e:
                    print(f"{direction}! bad packet: {e}")

            # Log raw traffic to bin if enabled (raw chunks)
            if traffic_bin is not None:
                traffic_bin.write(data)
                if config.flush_bin[flush_bin_idx]:
                    traffic_bin.flush()

        # Forward raw data unchanged
        try:
            write_sock.sendall(data)
        except:
            break

    # Final flush to ensure all data is written before exit
    if config.flush_bin[flush_bin_idx]:
        with config.lock:
            if traffic_txt is not None:
                traffic_txt.flush()
            if traffic_bin is not None:
                traffic_bin.flush()

    print(f"{direction} task exited")
    read_sock.close()


def main():
    parser = argparse.ArgumentParser(description="Terraria Protocol Proxy")
    parser.add_argument(
        "server",
        nargs="?",
        default="127.0.0.1:7777",
        help="Target server address (host:port)",
    )
    parser.add_argument(
        "bind",
        nargs="?",
        default="127.0.0.1:8888",
        help="Proxy bind address (host:port)",
    )
    parser.add_argument(
        "--save",
        choices=["bin", "txt"],
        default=None,
        help="Save format: 'bin' (raw binary), 'txt' (parsed text)",
    )
    parser.add_argument(
        "--flush",
        choices=["in", "out", "both"],
        default=None,
        help="Auto-flush traffic files on startup: 'in' (CTS/client->server), 'out' (STC/server->client), 'both'",
    )
    args = parser.parse_args()

    def parse_addr(addr_str: str) -> tuple[str, int]:
        parts = addr_str.rsplit(":", 1)
        if len(parts) != 2:
            raise ValueError(
                f"Invalid address format '{addr_str}'. Expected 'host:port'"
            )
        host = parts[0].strip()
        if not host:
            raise ValueError(f"Empty host in '{addr_str}'")
        try:
            port = int(parts[1].strip())
        except ValueError:
            raise ValueError(f"Invalid port '{parts[1].strip()}' in '{addr_str}'")
        if not (1 <= port <= 65535):
            raise ValueError(f"Port {port} out of range (1-65535) in '{addr_str}'")
        return (host, port)

    try:
        SERVER_ADDR = parse_addr(args.server)
        BIND_ADDR = parse_addr(args.bind)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    with config.lock:
        save_mode = args.save
        if save_mode == "bin":
            config.server_traffic_bin = open("server-traffic.bin", "wb")
            config.client_traffic_bin = open("client-traffic.bin", "wb")
        elif save_mode == "txt":
            config.server_traffic_txt = open(
                "server-traffic.txt", "w", encoding="utf-8"
            )
            config.client_traffic_txt = open(
                "client-traffic.txt", "w", encoding="utf-8"
            )
            config.both_traffic_txt = open("both-traffic.txt", "w", encoding="utf-8")

        # Auto-flush if requested
        if args.flush:
            if args.flush == "in":
                config.flush_bin[1] = True
                config.flush_txt[1] = True
            elif args.flush == "out":
                config.flush_bin[0] = True
                config.flush_txt[0] = True
            elif args.flush == "both":
                config.flush_bin[0] = config.flush_bin[1] = True
                config.flush_txt[0] = config.flush_txt[1] = True
                config.flush_both_txt = True

    print(f"Proxy bind: {BIND_ADDR}")
    print(f"Target server: {SERVER_ADDR}")
    print(f"Binding socket to {BIND_ADDR}...")
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(BIND_ADDR)
    listener.listen(1)
    print(f"Socket bound to {BIND_ADDR}. Accepting incoming client connection...")
    print("Launching input thread (UIT)...")
    input_thread = threading.Thread(target=user_input, daemon=True)
    input_thread.start()
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
    print("Launching Server-to-Client task (STC)...")
    stc_thread = threading.Thread(
        target=forward,
        args=(
            "STC",
            server_sock,
            client_sock,
            config.server_parser,
            config.dbg_in_tags,
        ),
        daemon=True,
    )
    stc_thread.start()
    print("Launching Client-to-Server task (CTS)...")
    cts_thread = threading.Thread(
        target=forward,
        args=(
            "CTS",
            client_sock,
            server_sock,
            config.client_parser,
            config.dbg_out_tags,
        ),
        daemon=True,
    )
    cts_thread.start()
    try:
        stc_thread.join()
        cts_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down proxy gracefully...")


if __name__ == "__main__":
    main()
