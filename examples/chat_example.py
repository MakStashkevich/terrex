import threading
import time

from terrex import Terrex
from terrex.event import Event
from terrex.net.module import NetTextModule
from terrex.world.map_helper import MapHelper

import asyncio


async def main():
    # Create a Terrex object and used as async client
    async with Terrex("127.0.0.1", 8888, server_password="4444") as client:
        # Send message to chat after connected to Terraria server
        await client.send_message("I'm alive!")

        # Use chat event for handle messages
        @client.on(Event.Chat)
        async def chat(module: NetTextModule):
            if client.player.id == module.author_id:
                # ignore self messages
                return

            msg = module.text.text
            print(f"Chat message: {msg}")

            # Do something with the message
            # In this case, stop the bot if the word "Stop" occurs
            if "stop" in msg:
                await client.send_message("Goodbye!")
                await client.stop()

            # Or reply with the message "hello world!" if you encounter the word "hello" :-)
            elif "hello" in msg:
                await client.send_message("Hello world!")

        # Keep runned process until disconnected
        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
