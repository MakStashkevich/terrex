import time
from terrex import Terrex
from terrex.events import Events

# used with proxy on port 8888
bot = Terrex('127.0.0.1', 8888)
event = bot.get_event_manager()

@event.on_event(Events.ItemOwnerChanged)
def logged_in(event_id, data):
    print(data)

@event.on_event(Events.ItemDropped)
def item_dropped(event_id, data):
    print("New item dropped")

@event.on_event(Events.ItemDropUpdate)
def item_drop_update(event_id, data):
    print("Update on item")
    print("X: " + str(data.x) + " Y: " + str(data.y))

bot.start()

try:
    while bot.client.running:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Остановка бота...")
    bot.stop()