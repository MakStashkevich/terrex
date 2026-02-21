import asyncio

from terrex import Terrex


async def main():
    # Create a Terrex object used with proxy on port 8888
    async with Terrex('127.0.0.1', 8888, server_password="4444") as client:
        # @client.on(UpdateOwnerItem)
        # def logged_in(data: ItemOwnerChangedEvent):
        #     print(data)

        # @client.on(NewDropped(item=123))
        # def item_dropped(data: ItemDroppedEvent):
        #     print("New item dropped")

        # @client.on(UpdateDropped)
        # def item_drop_update(data: ItemDropUpdateEvent):
        #     print("Update on item")
        #     print("X: " + str(data.x) + " Y: " + str(data.y))

        # Keep the process running until disconnected
        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
