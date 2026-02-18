import time

from terrex import Terrex
from terrex.event import Event
from terrex.net.module import NetTextModule

# Create a Terrex object
# used with proxy on port 8888
terrex = Terrex("127.0.0.1", 8888, server_password="4444")
event = terrex.get_event_manager()


# Connect a function to an event using a decorator
@event.on_event(Event.Chat)
def chat(module: NetTextModule):
    if terrex.player.id == module.author_id:
        # ignore self messages
        return

    msg = module.text.text
    print(f"Chat message: {msg}")

    # Do something with the message
    # In this case, stop the bot if the word "Stop" occurs
    if "stop" in msg:
        terrex.stop()

    # Or reply with the message "hello world!" if you encounter the word "hello" :-)
    elif "hello" in msg:
        terrex.send_message("hello world!")


# Start the bot
terrex.start()

# And wait
try:
    while terrex.client.running:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping bot...")
    terrex.stop()
