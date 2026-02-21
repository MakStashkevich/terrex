import threading
import time

from terrex import Terrex
from terrex.event import Event
from terrex.net.module import NetTextModule
from terrex.world.map_helper import MapHelper

# Create a Terrex object used with proxy on port 8888
with Terrex("127.0.0.1", 8888, server_password="4444") as client:
    event = client.get_event_manager()

    # Connect a function to an event using a decorator
    @event.on_event(Event.Chat)
    def chat(module: NetTextModule):
        if client.player.id == module.author_id:
            # ignore self messages
            return

        msg = module.text.text
        print(f"Chat message: {msg}")

        # Do something with the message
        # In this case, stop the bot if the word "Stop" occurs
        if "stop" in msg:
            client.send_message("goodbye!")
            client.stop()

        # Or reply with the message "hello world!" if you encounter the word "hello" :-)
        elif "hello" in msg:
            client.send_message("hello world!")

        elif "map" in msg:

            def generate_map():
                client.send_message("start generate map image...")
                img = MapHelper.draw_world_image()
                img.save("world.png", compress_level=0)
                client.send_message("map image successful generated!")

            thread = threading.Thread(target=generate_map, daemon=True)
            thread.start()

    # Keep runned process until disconnected
    client.run_until_disconnected()
