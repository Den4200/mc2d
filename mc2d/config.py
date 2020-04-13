import json
from pathlib import Path

import toml


CONFIG = toml.load('config.toml')

TITLE = CONFIG['title']
WINDOW_SIZE = (
    CONFIG['window_size']['x'],
    CONFIG['window_size']['y']
)
FULLSCREEN = CONFIG['window_size']['fullscreen']
SCALING = CONFIG['scaling']
VIEWPORT = CONFIG['viewport']

CHUNK_SIZE = CONFIG['world']['chunk_size_x'], CONFIG['world']['chunk_size_y']

MAX_STACK_SIZE = CONFIG['max_stack_size']
TILE_SIZE = 32

GRAVITY = 1

PLAYER_SIZE = (32, 64)
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 10

ASSETS = Path('assets')

MAIN_MENU_BG = ASSETS / 'splash_screen.png'

LEAVES = ASSETS / 'leaves'
GRASS = ASSETS / 'grass'
WOOD = ASSETS / 'wood'
PLAYER = ASSETS / 'player'
UI = ASSETS / 'ui'

PLAY_BUTTON_RELEASED = UI / 'play_button_released.png'
PLAY_BUTTON_PRESSED = UI / 'play_button_pressed.png'

NEW_WORLD_BUTTON_RELEASED = UI / 'new_world_button_released.png'
NEW_WORLD_BUTTON_PRESSED = UI / 'new_world_button_pressed.png'

LOAD_WORLD_BUTTON_RELEASED = UI / 'load_world_button_released.png'
LOAD_WORLD_BUTTON_PRESSED = UI / 'load_world_button_pressed.png'

SELECTION_BOX = UI / 'selection_box.png'
INVENTORY = UI / 'inventory.png'

TREE_SHAPES = json.loads((ASSETS / 'tree_shapes.json').read_text())

BLOCK_PATHS = {
    'dirt': str(ASSETS / 'dirt.png'),
    'grass': str(GRASS / 'grass_2.png'),
    'oak_wood': str(WOOD / 'oak_wood.png'),
    'oak_leaves': str(LEAVES / 'oak_leaves.png')
}

BLOCK_IDS = {
    1: 'dirt',
    2: 'grass',
    3: 'oak_wood',
    4: 'oak_leaves'
}
