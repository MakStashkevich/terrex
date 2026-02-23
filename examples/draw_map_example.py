import asyncio
import time

from PIL import Image

from typing import Any

from terrex import Terrex
from terrex.event.filter import IncomingMessage, NewMessage
from terrex.net.enum.section_size import SectionSize
from terrex.net.structure.rgb import Rgb
from terrex.net.structure.vec2 import Vec2
from terrex.world.map_helper import MapHelper
from terrex.world.world import World


async def draw_map_image(client: Terrex) -> Image.Image:
    """Heavy synchronous task demonstrating that sync handlers run in separate threads."""
    world = client.world
    if not isinstance(world, World):
        raise TypeError("world must be a World instance")

    height: int = max(1, world.max_tiles_y)
    width: int = max(1, world.max_tiles_x)

    def section_range(start: int, end: int, step: int):
        while start <= end:
            yield start
            start += step

    sections_y = list(section_range(SectionSize.Height, height, SectionSize.Height))
    sections_x = list(section_range(SectionSize.Width, width, SectionSize.Width))
    total_sections = len(sections_y) * len(sections_x)
    processed_sections = 0
    last_scan_message = 0.0

    # teleports for all world to collect all sections with tiles data
    for section_y in sections_y:
        for section_x in sections_x:
            # teleport to center section
            section_center = Vec2.from_tile_pos(section_x - (SectionSize.Width / 2), section_y - (SectionSize.Height / 2))
            await client.teleport(section_center)
            await asyncio.sleep(0.1)

            processed_sections += 1
            current_time = time.time()
            if current_time - last_scan_message >= 5.0:
                percent_done = (processed_sections / total_sections) * 100 if total_sections > 0 else 100.0
                await client.send_message(f"Map scanning progress: {percent_done:.1f}%", wait=True)
                last_scan_message = current_time

    # wait latest sections
    await asyncio.sleep(3)

    # return to spawn
    await client.teleport(Vec2.from_tile_pos(world.spawn_x, world.spawn_y))

    total_pixels = width * height
    processed_pixels = 0
    last_draw_message = 0.0

    # draw all tiles on image
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            try:
                mt = MapHelper.create_map_tile(world, x, y, 255)
                color = MapHelper.get_map_tile_xna_color(mt)
            except Exception as e:
                print(e)
                print(mt)
                color = Rgb.get_Red()
            pixels[x, y] = (color.r, color.g, color.b)

            processed_pixels += 1
            current_time = time.time()
            if current_time - last_draw_message >= 5.0:
                percent_done = (processed_pixels / total_pixels) * 100 if total_pixels > 0 else 100.0
                await client.send_message(f"Image creation progress: {percent_done:.1f}%", wait=True)
                last_draw_message = current_time
    img.save("world.png", compress_level=0)
    return img


async def main() -> None:
    """Main entry point to the draw map example."""
    host: str = "127.0.0.1"
    port: int = 8888
    password: str = "4444"

    async with Terrex(host, port, server_password=password) as client:

        @client.on(NewMessage(r"^map$") & IncomingMessage())
        async def handle_map_command_from_other_player() -> None:
            """Generates map image on 'map' command without blocking event loop."""
            await client.send_message("Starting map image generation...", True)
            await draw_map_image(client)
            await client.send_message("Map image successfully generated!")

        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
