import threading
import time

from PIL import Image

from terrex import Terrex
from terrex.event import Event
from terrex.net.module import NetTextModule
from terrex.world.map_helper import MapHelper

import asyncio

from terrex.world.world import World


# heavy task -> blocked all processes
def draw_map_image(world: World) -> Image.Image:
    # print(f"tile_position={MapHelper.tile_position}, wall_position={MapHelper.wall_position}, liquid_position={MapHelper.liquid_position}, sky_position={MapHelper.sky_position}")
    # print(f"dirt_position={MapHelper.dirt_position}, rock_position={MapHelper.rock_position}, hell_position={MapHelper.hell_position}")

    if not isinstance(world, World):
        return

    height = max(1, world.max_tiles_y)
    width = max(1, world.max_tiles_x)
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            mt = MapHelper.create_map_tile(x, y, 255)
            color = MapHelper.get_map_tile_xna_color(mt)
            rgb = (color.r, color.g, color.b)
            pixels[x, y] = rgb
    img.save("world.png", compress_level=0)
    return img


async def main():
    # Create a Terrex object and used as async client
    async with Terrex("127.0.0.1", 8888, server_password="4444") as client:
        # Send message to chat after connected to Terraria server
        await client.send_message("I'm alive!")

        # Use chat event for handle messages
        @client.on(Event.Chat)
        def chat_draw_map(module: NetTextModule):  # use sync func
            if client.player.id == module.author_id:
                # ignore self messages
                return

            msg = module.text.text
            if not "map" in msg:
                return

            # set wait=True to make sure that the message is 100% delivered BEFORE start draw map
            client.call_async(client.send_message, "Start generate map image...", True)
            draw_map_image(client.world)
            client.call_async(client.send_message, "Map image successful generated!")

        # Keep runned process until disconnected
        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
