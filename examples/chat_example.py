import asyncio

from typing import Any

from terrex import Terrex
from terrex.event.filter import (
    IncomingMessage,
    NewMessage,
    OutgoingMessage,
)
from terrex.event.types import ChatEvent


async def main() -> None:
    """Main entry point for the chat example."""
    host: str = "127.0.0.1"
    port: int = 8888
    password: str = "4444"

    async with Terrex(host, port, server_password=password) as client:
        await client.send_message("I'm alive!")

        @client.on(NewMessage())
        async def handle_all_chat_messages(event: ChatEvent) -> None:
            """Prints every chat message received or sent."""
            print(f"Chat message: {event.text}")

        @client.on(NewMessage(r"(?i)^(.*)alive(.*)$") & OutgoingMessage())
        async def handle_own_alive_message() -> None:
            """Responds with laughter to own chat messages containing 'alive' (case-insensitive)."""
            await client.send_message("Ha-ha-ha!!!")

        @client.on(NewMessage(r"^(hello|hi)$") & IncomingMessage())
        async def handle_greeting_from_other_player() -> None:
            """Responds to 'hello' or 'hi' from other players."""
            await client.send_message("Hello world!")

        @client.on(NewMessage(r"^(stop|bye)$") & IncomingMessage())
        async def handle_farewell_from_other_player() -> None:
            """Responds to 'stop' or 'bye' from other players and stops the client."""
            await client.send_message("Goodbye!")
            await client.stop()

        @client.on(NewMessage() & IncomingMessage(player_id=1))
        async def handle_messages_from_player_1() -> None:
            """Responds to all incoming messages from player with id=1."""
            await client.send_message("Hello player with id=1!")

        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
