import asyncio

from PIL import Image

from typing import Any

from terrex import Terrex
from terrex.event.filter import IncomingMessage, NewMessage
from terrex.world.map_helper import MapHelper
from terrex.world.world import World


def draw_map_image(world: World) -> Image.Image:
    """Heavy synchronous task demonstrating that sync handlers run in separate threads."""
    if not isinstance(world, World):
        raise TypeError("world must be a World instance")

    height = max(1, world.max_tiles_y)
    width = max(1, world.max_tiles_x)
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            mt = MapHelper.create_map_tile(world, x, y, 255)
            color = MapHelper.get_map_tile_xna_color(mt)
            pixels[x, y] = (color.r, color.g, color.b)
    img.save("world.png", compress_level=0)
    return img


async def main() -> None:
    """Main entry point demonstrating sync handler with heavy computation."""
    host: str = "127.0.0.1"
    port: int = 8888
    password: str = "4444"

    async with Terrex(host, port, server_password=password) as client:

        @client.on(NewMessage(r"^map$") & IncomingMessage())
        def handle_map_command_from_other_player() -> None:
            """Sync handler: generates map image on 'map' command without blocking event loop."""
            client.call_async(client.send_message, "Starting map image generation...", True)
            draw_map_image(client.world)
            client.call_async(client.send_message, "Map image successfully generated!")

        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
