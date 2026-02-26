# Terrex

Programmable automation client for Terraria servers.

[![PyPI version](https://badge.fury.io/py/terrex.svg)](https://badge.fury.io/py/terrex)

![Terrex logo](https://raw.githubusercontent.com/makstashkevich/terrex/master/assets/logo.jpg)

---

## What is Terrex?

Terrex is a Python framework for building programmable Terraria agents (bots).

It provides a clean event-driven API for connecting to servers, reacting to world state,
parsing packets and executing scripted behaviors.

Originally inspired by an archived [TerraBot](https://github.com/flammified/terrabot) project by Alexander Freeman (MIT licensed) (inactive for ~10 years),  
Terrex is a modernized, extended and actively developed fork focused on:

* automation
* simulation
* protocol control
* scalable multi-agent systems

Think of it as a runtime for Terraria agents — not just a bot.

---

## Installation

```bash
pip3 install terrex
````

---

## Core Features

* Connect to Terraria servers as a client
* Full chat interaction
* Event-driven packet handling
* Live world & player state parsing
* Item & tile updates tracking
* Programmatic movement (teleport + control layer)
* Extensible event system for custom logic

---

## Minimal Example

A basic bot that connects to a server and reacts to chat messages:

```python
import asyncio

from terrex import Terrex
from terrex.event.filter import NewMessage
from terrex.event.types import ChatEvent

async def main() -> None:
    async with Terrex("127.0.0.1", 7777) as client:
        @client.on(NewMessage())
        async def on_chat(event: ChatEvent) -> None:
            print(event.text)

            if "stop" in event.text.lower():
                await client.stop()

        await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
```

More examples are available in the `examples/` directory.

---

## Project Philosophy

Terrex is built as an automation engine — not a cheat client.

Primary use cases include:

* programmable agents
* server testing & simulation
* AI experiments
* scripted behaviors
* world interaction automation

Anything else is simply an emergent property.

---

## Contributing

Terrex is under active development and contributions are welcome.

Current high-priority areas:

* NPC packet parsing
* Item interactions & drops
* Player synchronization packets
* Tile placement & world modification
* Movement & physics layer

Packet documentation reference:
[https://github.com/MakStashkevich/terrex/blob/master/docs/packets.md](https://github.com/MakStashkevich/terrex/blob/master/docs/packets.md)

---

## Origins

Terrex is based on a fork of the original [TerraBot](https://github.com/flammified/terrabot) project by Alexander Freeman (MIT licensed) (now archived and unmaintained).
The codebase has been refactored, extended and re-architected for modern Python workflows.

---

## Roadmap (high level)

* stable protocol layer
* multi-agent orchestration
* scripting behaviors (FSM / behavior trees)
* performance scaling
* cleaner API surface