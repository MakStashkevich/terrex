import time

from terrex import Terrex
from terrex.event import Event

# Create a Terrex object used with proxy on port 8888
with Terrex('127.0.0.1', 8888, server_password="4444") as client:
    # @client.on(Event.ItemOwnerChanged)
    # def logged_in(data):
    #     print(data)

    @client.on(Event.ItemDropped)
    def item_dropped(data):
        print("New item dropped")

    @client.on(Event.ItemDropUpdate)
    def item_drop_update(data):
        print("Update on item")
        print("X: " + str(data.x) + " Y: " + str(data.y))

    # Keep runned process until disconnected
    client.run_until_disconnected()
