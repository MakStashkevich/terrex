from terrex import Terrex
from terrex.event.message import NewMessage
from terrex.event.player import FromCurrentPlayer, FromOtherPlayer

import asyncio

from terrex.event.types import ChatEvent


async def main():
    # Create a Terrex object and used as async client
    async with Terrex("127.0.0.1", 8888, server_password="4444") as client:
        # Send message to chat after connected to Terraria server
        await client.send_message("I'm alive!")

        @client.on(NewMessage())
        async def handle_all_chat_messages(event: ChatEvent):
            """Prints every chat message received or sent."""
            msg = event.text
            print(f"Chat message: {msg}")

        @client.on(NewMessage(r"(?i)^(.*)alive(.*)$") & FromCurrentPlayer())
        async def handle_own_alive_message():
            """Responds with laughter to own chat messages containing 'alive' (case-insensitive)."""
            await client.send_message("Ha-ha-ha!!!")

        @client.on(NewMessage(r"^(hello|hi)$") & FromOtherPlayer())
        async def handle_greeting_from_other_player():
            """Responds to 'hello' or 'hi' from other players."""
            await client.send_message("Hello world!")

        @client.on(NewMessage(r"^(stop|bye)$") & FromOtherPlayer())
        async def handle_farewell_from_other_player():
            """Responds to 'stop' or 'bye' from other players and stops the client."""
            await client.send_message("Goodbye!")
            await client.stop()

        # Keep the process running until disconnected
        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
