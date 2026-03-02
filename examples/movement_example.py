import asyncio

from terrex import Terrex
from terrex.event.filter import IncomingMessage, NewMessage
from terrex.event.filter.player import ControlBy, ControlPlayer
from terrex.event.types import PlayerControlUpdateEvent
from terrex.net.structure.vec2 import Vec2

host: str = "127.0.0.1"
port: int = 8888
password: str = "4444"

state = {"seek_enabled": False}

client = Terrex(host, port, server_password=password)


@client.on(NewMessage(r"^move$") & IncomingMessage())
async def handle_move_command() -> None:
    client.move_to(Vec2(client.player.position.x + 160, client.player.position.y - 160))


@client.on(NewMessage(r"^seek$") & IncomingMessage())
async def handle_seek_command() -> None:
    state["seek_enabled"] = not state["seek_enabled"]
    await client.send_message(f"Seek {'enabled' if state["seek_enabled"] else 'disabled'}.")


@client.on(ControlPlayer() & ControlBy(player_id=1))
async def handle_seek_player(event: PlayerControlUpdateEvent) -> None:
    if state["seek_enabled"]:
        client.move_to(event.position)


async def main() -> None:
    """Main entry point to the draw map example."""
    async with client:
        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
