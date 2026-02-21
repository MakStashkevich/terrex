from PIL import Image

from terrex import Terrex
from terrex.event.message import NewMessage
from terrex.event.player import FromOtherPlayer
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

        # Use chat event to handle "map" command from other players
        @client.on(NewMessage(r"^map$") & FromOtherPlayer())
        def handle_map_command_from_other_player():  # synchronous handler to avoid event loop blocking
            """
            Generates and saves a PNG map image of the world when "map" is received from other players.
            Uses a synchronous function for heavy computation.
            Sends status messages before and after generation.
            """
            # Ensure the start message is delivered before starting the heavy task
            client.call_async(client.send_message, "Starting map image generation...", True)
            draw_map_image(client.world)
            client.call_async(client.send_message, "Map image successfully generated!")

        # Keep the process running until disconnected
        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
