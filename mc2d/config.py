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

SELECTION_BOX = UI / 'selection_box.png'
INVENTORY = UI / 'inventory.png'

TREE_SHAPES = json.loads((ASSETS / 'tree_shapes.json').read_text())

BLOCK_PATHS = {
    'grass': str(GRASS / 'grass_2.png'),
    'oak_wood': str(WOOD / 'oak_wood.png'),
    'oak_leaves': str(LEAVES / 'oak_leaves.png')
}

BLOCK_IDS = {
    1: 'grass',
    2: 'oak_wood',
    3: 'oak_leaves'
}
