import heapq
from dataclasses import dataclass
from typing import List, Optional
import itertools
import numpy as np
from PIL import Image, ImageDraw

from terrex.net.structure.vec2 import Vec2
from terrex.net.tile_npc_data import TileNPCData
from terrex.world.world import World
from terrex.player.player import Player
from terrex.net.structure.tile import Tile

tile_data = TileNPCData()

# Параметры карты и игрока
TILE_SIZE = 16
MAP_WIDTH = 30
MAP_HEIGHT = 15

# Генерация карты
# 0 = пусто, 1 = solid, 2 = solidTop
MAP = np.zeros((MAP_HEIGHT, MAP_WIDTH), dtype=np.uint8)

# Горизонтальные платформы solidTop (type=19)
for y in range(1, MAP_HEIGHT - 1, 2):
    for x_base in range(4, MAP_WIDTH - 3, 5):
        MAP[y, x_base : x_base + 3] = 19  # Wood Platform

# Пол - solid (type=1)
MAP[MAP_HEIGHT - 1, :] = 1  # Stone Block

GRAVITY = 0.4
MAX_FALL_SPEED = 10.0
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 42
JUMP_SPEED = 5.01

world = World()
world.max_tiles_x = MAP_WIDTH
world.max_tiles_y = MAP_HEIGHT

for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if MAP[y, x] > 0:
            world.tiles.set(x, y, Tile(type=int(MAP[y, x])))


def test_movement(start_pos: Vec2, goal_pos: Vec2, filename: str = None):
    player = Player(world)
    player.position = start_pos
    player.velocity = Vec2(0, 0)
    player._target_position = goal_pos

    print(f"Test to {goal_pos}: start at {start_pos}")

    ticks = 0
    max_ticks = 2000
    positions = []

    while player.position.distance_to(goal_pos) > TILE_SIZE / 2 and ticks < max_ticks:
        old_pos = Vec2(player.position.x, player.position.y)
        player.update(ticks)
        if player.position != old_pos:
            positions.append((player.position.x, player.position.y))
        if ticks % 10 == 0:
            print(
                f"Tick {ticks}: pos={player.position}, vel={player.velocity}, control L/R/J/D/U={player.control.left}/{player.control.right}/{player.control.jump}/{player.control.down}/{player.control.up}, on_ground={player.is_on_ground()}, can_stand={player.can_stand(player.position)}"
            )
        ticks += 1

    reached = player.position.distance_to(goal_pos) < TILE_SIZE  # approx
    print(f"Reached in {ticks} ticks: {reached}, final pos {player.position}")

    if filename:
        draw_pil(positions, filename)

    return reached, ticks


def draw_pil(positions: List[tuple], filename: str):
    width = MAP_WIDTH * TILE_SIZE
    height = MAP_HEIGHT * TILE_SIZE
    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    # тайлы
    for y, row in enumerate(MAP):
        for x, t in enumerate(row):
            color = None
            if t == 1:  # Stone block
                color = (0, 0, 0)
            elif t == 19:  # Wood Platform
                color = (128, 128, 128)
            if color:
                draw.rectangle(
                    [x * TILE_SIZE, y * TILE_SIZE, (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE],
                    fill=color,
                )

    # путь
    if positions:
        points = positions
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=(255, 0, 0), width=2)
        # старт
        sx, sy = positions[0]
        draw.rectangle(
            [sx, sy, sx + PLAYER_WIDTH, sy + PLAYER_HEIGHT], fill=(0, 0, 255), outline=(0, 0, 0)
        )

    img.save(filename)


# Тесты
start_pos = Vec2(0, (MAP_HEIGHT - 1) * TILE_SIZE - PLAYER_HEIGHT)
goal_pos = Vec2(27 * TILE_SIZE, 12 * TILE_SIZE - PLAYER_HEIGHT)
test_movement(start_pos, goal_pos, "test_path1.png")

# Test 2: right upper to left lower
start_pos2 = Vec2((MAP_WIDTH - 3) * TILE_SIZE, 3 * TILE_SIZE - PLAYER_HEIGHT)
goal_pos2 = Vec2(0, (MAP_HEIGHT - 1) * TILE_SIZE - PLAYER_HEIGHT)
test_movement(start_pos2, goal_pos2, "test_path2.png")

# Test 3: right bottom -> center
start_pos3 = Vec2((MAP_WIDTH - 2) * TILE_SIZE, (MAP_HEIGHT - 1) * TILE_SIZE - PLAYER_HEIGHT)
goal_pos3 = Vec2((MAP_WIDTH // 2) * TILE_SIZE, (MAP_HEIGHT // 2) * TILE_SIZE - PLAYER_HEIGHT)
reached3, ticks3 = test_movement(start_pos3, goal_pos3, "test_path3.png")
assert reached3, f"Test 3 failed in {ticks3} ticks"
print(f"Test 3 passed in {ticks3} ticks")

# Test 4: left center -> right center
center_y = 7 * TILE_SIZE - PLAYER_HEIGHT
start_pos4 = Vec2(0, center_y)
goal_pos4 = Vec2((MAP_WIDTH - 2) * TILE_SIZE, center_y)
reached4, ticks4 = test_movement(start_pos4, goal_pos4, "test_path4.png")
assert reached4, f"Test 4 failed in {ticks4} ticks"
print(f"Test 4 passed in {ticks4} ticks")

# Test 5: left floor -> right floor
start_pos5 = Vec2(0, (MAP_HEIGHT - 1) * TILE_SIZE - PLAYER_HEIGHT)
goal_pos5 = Vec2((MAP_WIDTH - 2) * TILE_SIZE, (MAP_HEIGHT - 1) * TILE_SIZE - PLAYER_HEIGHT)
reached5, ticks5 = test_movement(start_pos5, goal_pos5, "test_path5.png")
assert reached5, f"Test 5 failed in {ticks5} ticks"
print(f"Test 5 passed in {ticks5} ticks")

# Test 6: center floor -> center top
start_pos6 = Vec2((MAP_WIDTH // 2) * TILE_SIZE, (MAP_HEIGHT - 1) * TILE_SIZE - PLAYER_HEIGHT)
goal_pos6 = Vec2((MAP_WIDTH // 2) * TILE_SIZE, 3 * TILE_SIZE - PLAYER_HEIGHT)
reached6, ticks6 = test_movement(start_pos6, goal_pos6, "test_path6.png")
assert reached6, f"Test 6 failed in {ticks6} ticks"
print(f"Test 6 passed in {ticks6} ticks")

print("All tests completed successfully.")
