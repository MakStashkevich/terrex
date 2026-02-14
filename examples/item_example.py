import time

from terrex import Terrex
from terrex.events import Event

# Create a Terrex object
# used with proxy on port 8888
terrex = Terrex('127.0.0.1', 8888, server_password="4444")
event = terrex.get_event_manager()

# @event.on_event(Event.ItemOwnerChanged)
# def logged_in(data):
#     print(data)

@event.on_event(Event.ItemDropped)
def item_dropped(data):
    print("New item dropped")

@event.on_event(Event.ItemDropUpdate)
def item_drop_update(data):
    print("Update on item")
    print("X: " + str(data.x) + " Y: " + str(data.y))

terrex.start()

try:
    while terrex.client.running:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping bot...")
    terrex.stop()