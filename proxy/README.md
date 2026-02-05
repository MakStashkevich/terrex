# Terraria Protocol Proxy

## Overview

This directory contains a transparent **TCP proxy server** for intercepting, parsing, logging, and dumping network traffic between a [Terraria](https://terraria.org/) client and server. It leverages the `terrex` library for packet parsing and supports selective debugging of specific packet types.

The proxy acts as a man-in-the-middle:
- Listens on `127.0.0.1:8888` for incoming client connections.
- Forwards traffic to the real server at `127.0.0.1:7777` (according to the standard, a local server is used, but you can install any other one) (configurable in [`proxy.py`](proxy.py)).
- Parses packets incrementally using [`IncrementalParser`](parser.py).
- Logs parsed packet details (if enabled via tags).
- Dumps raw traffic to `server-traffic.bin` (server -> client) and `client-traffic.bin` (client -> server).

## Features

- **Transparent proxying**: No client modifications required; connect client to proxy bind address.
- **Packet parsing**: Uses [`terrex.packets`](../terrex/packets) registry to deserialize packets.
- **Selective console logging**: Toggle per-packet-ID logging via commands.
- **Optional traffic saving**:
  - `--save=bin`: Raw binary dumps (`server-traffic.bin`, `client-traffic.bin`).
  - `--save=txt`: Parsed text logs (`server-traffic.txt`, `client-traffic.txt`) with format:
    ```
    ---0x34 PLAYER_HP ---
    {'player_id': 0, 'hp': 100, 'max_hp': 100}

    ---0x17 NPC_UPDATE ---
    {...}
    ```
- **Traffic flushing**:
  - `--flush=in/out/both`: Enable continuous flushing of traffic files after each write (CTS/STC/both directions).
  - Automatic final flush on client disconnect to ensure all data is persisted.
- **Interactive console**: Control logging, flush/save files.
- **Thread-safe**: Bidirectional forwarding with locking.

## Prerequisites

- Python 3.8+
- `terrex` library (install via `pip install -e .` from project root or ensure it's in `PYTHONPATH`).

## Quick Start

1. **Navigate to proxy directory**:
   ```
   cd proxy
   ```

2. **Run the proxy** (examples):
   ```
   # Default: proxy 127.0.0.1:8888 -> 127.0.0.1:7777
   python proxy.py

   # Custom server
   python proxy.py terraria.makstashkevich.com:7777

   # Custom server + bind
   python proxy.py terraria.makstashkevich.com:7777 0.0.0.0:8888

   # With saving and auto-flush
   python proxy.py --save=txt --flush=both
   ```
   Output example:
   ```
   Proxy bind: ('127.0.0.1', 8888)
   Target server: ('terraria.makstashkevich.com', 7777)
   Binding socket to ('127.0.0.1', 8888)...
   Socket bound to ('127.0.0.1', 8888). Accepting incoming client connection...
   ```

3. **Connect Terraria client**:
   - Server IP/port: as specified in `bind` arg (default `127.0.0.1:8888`)

4. **Interact via console** (while proxy runs):
   ```
   help                # Show commands
   list                # List packet IDs and names
   show in 0x17        # Enable logging for NPC_UPDATE (CTS direction)
   hide out all        # Disable all STC logging
   flush               # Flush traffic dumps to disk
   nosave              # Stop saving traffic (close dump files)
   quit                # Exit
   ```

## Commands

| Command | Args | Description |
|---------|------|-------------|
| `help` | - | Show this help. |
| `quit` | - | Stop proxy and exit. |
| `show/hide` | `<in\|out\|both> <all\|TAG>` | Toggle logging for packets (e.g., `show both 34` for `PLAYER_HP`). TAG is decimal (0-255) or hex (e.g., `0x17`). |
| `list` | - | List all known packet IDs from [`PacketIds`](../terrex/packets/packet_ids.py). |
| `flush` | - | Flush **all** dump files (bin/txt). |
| `nosave` | - | Close **all** dump files. |

**Directions**:
- `in` / `CTS`: Client → Server (outgoing from client).
- `out` / `STC`: Server → Client (incoming to client).

**Logging example**:
```
STC> 34 PLAYER_HP {'player_id': 0, 'hp': 100, 'max_hp': 100}
CTS> 23 NPC_UPDATE {...}
```

## CLI Arguments

```
python proxy.py [SERVER] [BIND] [--save={bin|txt}] [--flush={in|out|both}]
```

- `SERVER` (default `127.0.0.1:7777`): Target `host:port`
- `BIND` (default `127.0.0.1:8888`): Listen `host:port`
- `--save` (default none): `bin` (raw), `txt` (parsed **all** packets)
- `--flush` (default none): `in` (CTS/client->server), `out` (STC/server->client), `both` — enable continuous flushing of traffic files

Other:
- Console logging: all packets enabled by default.
- `BUFFER_SIZE = 4096` [`proxy.py`](proxy.py:10)

## Files

- [`proxy.py`](proxy.py): Main proxy logic, forwarding threads, user input handler.
- [`config.py`](config.py): Shared config (parsers, traffic files, debug tags, lock).
- [`parser.py`](parser.py): Incremental packet parser using `terrex` registry.
- [`__init__.py`](__init__.py): Package initializer.

## Debugging Tips

- Use `list` to find packet IDs (e.g., `0x17` = `NPC_UPDATE`).
- Unknown packets are skipped or logged as `UnknownPacket`.
- Traffic dumps are raw binary; use hex editors or replay with tools.
- For high-traffic servers, tune `BUFFER_SIZE` or disable logging (`hide both all`).
- Use `--flush=both` with `--save=txt` for real-time readable logs (note: higher disk I/O).

## Limitations

- Single client connection (listens for 1 connection).
- No traffic modification (pure pass-through with logging).
- Relies on `terrex` for packet support; unsupported packets are skipped.

## License

Part of the terrex project ([LICENSE.txt](../LICENSE.txt)).