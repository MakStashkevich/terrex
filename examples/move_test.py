import heapq
from dataclasses import dataclass
from typing import List, Optional
import itertools
import numpy as np
from PIL import Image, ImageDraw

# Параметры карты и игрока
TILE_SIZE = 16
MAP_WIDTH = 30
MAP_HEIGHT = 15

# Генерация карты
# 0 = пусто, 1 = solid, 2 = solidTop
MAP = np.zeros((MAP_HEIGHT, MAP_WIDTH), dtype=np.uint8)

# Горизонтальные платформы solidTop (центральные ступеньки по центру col=15, шаг 2 тайла для достижимости)
for y in range(1, MAP_HEIGHT-1, 2):
    for x_base in range(4, MAP_WIDTH-3, 5):
        MAP[y, x_base:x_base+3] = 2

# Пол - solid
MAP[MAP_HEIGHT-1, :] = 1

# Физика (менять запрещено!!!)
GRAVITY = 0.4
MAX_FALL_SPEED = 4
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 32
JUMP_SPEED = 5
MOVE_SPEED = 2
DT = 1.0  # шаг = 1 tick Terraria для A* (полный обновление за шаг)

@dataclass
class Vec2:
    x: float
    y: float

@dataclass
class Node:
    cost: float
    position: Vec2
    velocity: Vec2
    on_ground: bool
    parent: Optional['Node'] = None
    action: Optional[str] = None

def can_stand(x: float, y: float) -> bool:
    left = int(x // TILE_SIZE)
    right = int((x + PLAYER_WIDTH - 1) // TILE_SIZE)
    top = int(y // TILE_SIZE)
    bottom = int((y + PLAYER_HEIGHT - 1) // TILE_SIZE)
    if bottom >= MAP_HEIGHT or left < 0 or right >= MAP_WIDTH or top < 0:
        return False
    for ty in range(top, bottom + 1):
        for tx in range(left, right + 1):
            tile = MAP[ty, tx]
            if tile == 1:
                return False
            if tile == 2 and ty == bottom and y + PLAYER_HEIGHT > (ty + 1) * TILE_SIZE:
                return False
    return True

def simulate_action(node: Node, action: str) -> Node:
    vx, vy = node.velocity.x, node.velocity.y
    x, y = node.position.x, node.position.y
    on_ground = node.on_ground

    if action == 'left':
        vx = -MOVE_SPEED
    elif action == 'right':
        vx = MOVE_SPEED
    elif action == 'none':
        vx = 0

    if action == 'jump' and on_ground:
        vy = -JUMP_SPEED
        on_ground = False

    # симуляция падения
    vy += GRAVITY
    if vy > MAX_FALL_SPEED:
        vy = MAX_FALL_SPEED

    nx = x + vx * DT
    ny = y + vy * DT

    # проверка коллизий снизу
    below = ny + PLAYER_HEIGHT
    tile_below_y = int(below // TILE_SIZE)
    tile_x1 = int(nx // TILE_SIZE)
    tile_x2 = int((nx + PLAYER_WIDTH - 1) // TILE_SIZE)
    on_ground_new = False

    if tile_below_y < MAP_HEIGHT:
        for tx in range(tile_x1, tile_x2 + 1):
            if tx < 0 or tx >= MAP_WIDTH:
                continue
            t = MAP[tile_below_y, tx]
            if t in [1, 2] and below <= (tile_below_y + 1) * TILE_SIZE:
                on_ground_new = True
                ny = tile_below_y * TILE_SIZE - PLAYER_HEIGHT
                vy = 0
                break

    if not can_stand(nx, ny):
        return None

    return Node(
        cost=node.cost + 1,
        position=Vec2(nx, ny),
        velocity=Vec2(vx, vy),
        on_ground=on_ground_new,
        parent=node,
        action=action
    )

def get_neighbors(node: Node) -> List[Node]:
    actions = ['none', 'left', 'right']
    if node.on_ground:
        actions.append('jump')
    neighbors = []
    for act in actions:
        n = simulate_action(node, act)
        if n:
            neighbors.append(n)
    return neighbors

def heuristic(pos: Vec2, goal: Vec2) -> float:
    return abs(goal.x - pos.x) + abs(goal.y - pos.y)

def find_path(start: Vec2, goal: Vec2) -> List[Node]:
    start_node = Node(cost=0, position=start, velocity=Vec2(0,0), on_ground=True)
    open_set = []
    counter = itertools.count()
    heapq.heappush(open_set, (heuristic(start, goal), next(counter), start_node))
    visited = set()

    max_reached_x = 0.0
    min_reached_y = float('inf')
    while open_set:
        _, _, current = heapq.heappop(open_set)
        old_min_y = min_reached_y
        max_reached_x = max(max_reached_x, current.position.x)
        min_reached_y = min(min_reached_y, current.position.y)
        if current.position.y < old_min_y:
            print(f"New min y: {current.position.y:.2f} (prev {old_min_y:.2f}), x={current.position.x:.1f}, cost={current.cost}, vel=({current.velocity.x:.1f},{current.velocity.y:.1f}), ground={current.on_ground}, action={current.action}")
        key = (int(current.position.x * 10), int(current.position.y * 10),
               int(current.velocity.x * 10), int(current.velocity.y * 10),
               current.on_ground)
        if key in visited:
            continue
        visited.add(key)

        # цель достигается, если близко к тайлу
        if abs(current.position.x - goal.x) <= TILE_SIZE and abs(current.position.y - goal.y) <= TILE_SIZE:
            path_nodes = []
            node = current
            while node.parent:
                path_nodes.append(node)
                node = node.parent
            return list(reversed(path_nodes))

        for neighbor in get_neighbors(current):
            h = heuristic(neighbor.position, goal)
            heapq.heappush(open_set, (neighbor.cost + h, next(counter), neighbor))

    print(f"No path found. Visited states: {len(visited)}")
    print(f"Max x reached: {max_reached_x}, Min y reached: {min_reached_y}")
    return []

def draw_pil(path_nodes: List[Node], filename="path.png"):
    width = MAP_WIDTH * TILE_SIZE
    height = MAP_HEIGHT * TILE_SIZE
    img = Image.new("RGB", (width, height), (30,30,30))
    draw = ImageDraw.Draw(img)

    # тайлы
    for y, row in enumerate(MAP):
        for x, t in enumerate(row):
            color = None
            if t == 1:
                color = (0,0,0)
            elif t == 2:
                color = (128,128,128)
            if color:
                draw.rectangle([x*TILE_SIZE, y*TILE_SIZE, (x+1)*TILE_SIZE, (y+1)*TILE_SIZE], fill=color)

    # путь
    if path_nodes:
        points = [(node.position.x + PLAYER_WIDTH/2, node.position.y + PLAYER_HEIGHT/2) for node in path_nodes]
        for i in range(len(points)-1):
            draw.line([points[i], points[i+1]], fill=(255,0,0), width=2)
        # старт
        start = path_nodes[0].position
        draw.rectangle([start.x, start.y, start.x+PLAYER_WIDTH, start.y+PLAYER_HEIGHT], fill=(0,0,255))

    img.save(filename)

# старт и цель
start_pos = Vec2(0, (MAP_HEIGHT-1)*TILE_SIZE - PLAYER_HEIGHT)
# цель на первой solidTop платформе (достижимая)
goal_pos = Vec2(27 * TILE_SIZE, 12 * TILE_SIZE - PLAYER_HEIGHT)
print(f"Goal tile: MAP[12,27] = {MAP[12,27]}")

path_nodes = find_path(start_pos, goal_pos)
print(f"Start: {start_pos}")
print(f"Goal: {goal_pos}")
print(f"Path length: {len(path_nodes)}")
if not path_nodes:
    print("No path found.")
draw_pil(path_nodes)

# Второй тест: правый верхний -> левый нижний (падение сквозь solidTop вниз)
start_pos2 = Vec2((MAP_WIDTH - 3) * TILE_SIZE, 3 * TILE_SIZE - PLAYER_HEIGHT)
goal_pos2 = Vec2(0, (MAP_HEIGHT-1)*TILE_SIZE - PLAYER_HEIGHT)
print(f"Test 2 Goal tile: MAP[MAP_HEIGHT-1,0] = {MAP[MAP_HEIGHT-1,0]}")
path_nodes2 = find_path(start_pos2, goal_pos2)
print(f"Start2: {start_pos2}")
print(f"Goal2: {goal_pos2}")
print(f"Path2 length: {len(path_nodes2)}")
draw_pil(path_nodes2, "path2.png")

# Тест 3: правый нижний -> центр карты
start_pos3 = Vec2((MAP_WIDTH - 1) * TILE_SIZE, (MAP_HEIGHT-1)*TILE_SIZE - PLAYER_HEIGHT)
goal_pos3 = Vec2((MAP_WIDTH // 2) * TILE_SIZE, (MAP_HEIGHT // 2) * TILE_SIZE - PLAYER_HEIGHT)
path_nodes3 = find_path(start_pos3, goal_pos3)
print(f"Path3 length: {len(path_nodes3)}")
draw_pil(path_nodes3, "path3.png")

# Тест 4: левый центр -> правый центр (горизонталь центр)
center_y = 7 * TILE_SIZE - PLAYER_HEIGHT  # approx center height stand
start_pos4 = Vec2(0, center_y)
goal_pos4 = Vec2((MAP_WIDTH - 1) * TILE_SIZE, center_y)
path_nodes4 = find_path(start_pos4, goal_pos4)
print(f"Path4 length: {len(path_nodes4)}")
draw_pil(path_nodes4, "path4.png")

# Тест 5: лево -> право по прямой (пол)
start_pos5 = Vec2(0, 192)
goal_pos5 = Vec2((MAP_WIDTH - 1) * TILE_SIZE, 192)
path_nodes5 = find_path(start_pos5, goal_pos5)
print(f"Path5 length: {len(path_nodes5)}")
draw_pil(path_nodes5, "path5.png")

# Тест 6: центр низ -> центр верх (вверх)
start_pos6 = Vec2((MAP_WIDTH // 2) * TILE_SIZE, 192)
goal_pos6 = Vec2((MAP_WIDTH // 2) * TILE_SIZE, 3 * TILE_SIZE - PLAYER_HEIGHT)
path_nodes6 = find_path(start_pos6, goal_pos6)
print(f"Path6 length: {len(path_nodes6)}")
draw_pil(path_nodes6, "path6.png")