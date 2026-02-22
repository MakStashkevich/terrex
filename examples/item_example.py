import asyncio

from typing import Any

from terrex import Terrex

from terrex.event.filter import (
    ItemDrop,
    ItemOwnedByMe,
    ItemOwnedByOther,
    UpdateItemDrop,
    UpdateItemOwner,
)

from terrex.event.types import (
    ItemDroppedEvent,
    ItemDropUpdateEvent,
    ItemOwnerChangedEvent,
)


async def main() -> None:
    """Main entry point for the item example."""

    host: str = "127.0.0.1"
    port: int = 8888
    password: str = "4444"

    async with Terrex(host, port, server_password=password) as client:

        @client.on(ItemDrop())
        async def on_item_dropped(event: ItemDroppedEvent) -> None:
            """Handles new item drops."""
            print(f"New item dropped: {event.item}")

        @client.on(UpdateItemDrop())
        async def on_item_drop_update(event: ItemDropUpdateEvent) -> None:
            """Handles updates to dropped items."""
            print(f"Update drop item: {event.item}")

        @client.on(UpdateItemOwner() & ItemOwnedByMe())
        async def on_item_owner_me_update(event: ItemOwnerChangedEvent) -> None:
            """Handles item owner changes for the current player."""
            print(f"Update item owner for current player: item_id={event.item_id}, owner_id={event.player_id}")

        @client.on(UpdateItemOwner() & ItemOwnedByOther())
        async def on_item_owner_other_update(event: ItemOwnerChangedEvent) -> None:
            """Handles item owner changes for other players."""
            print(f"Update item owner for other player: item_id={event.item_id}, owner_id={event.player_id}")

        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
