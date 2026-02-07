import time
from terrex import Terrex
from terrex.events import Event
from terrex.structures.load_net_module import LoadNetModuleServerText

# Create a Terrex object
# used with proxy on port 8888
bot = Terrex('127.0.0.1', 8888)
event = bot.get_event_manager()


# Connect a function to an event using a decorator
@event.on_event(Event.Chat)
def chat(module: LoadNetModuleServerText):
    msg = module.text.text
    # Do something with the message
    # In this case, stop the bot if the word "Stop" occurs
    print(msg)
    if "stop" in msg:
        bot.stop()


# Start the bot
bot.start()

# And wait
try:
    while bot.client.running:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping bot...")
    bot.stop()
