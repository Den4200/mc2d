from pathlib import Path

import toml


CONFIG = toml.load('config.toml')

TITLE = CONFIG['title']
WINDOW_SIZE = (
    CONFIG['window_size']['x'],
    CONFIG['window_size']['y']
)
SCALING = CONFIG['scaling']
VIEWPORT = CONFIG['viewport']

MAX_STACK_SIZE = CONFIG['max_stack_size']
TILE_SIZE = 32

GRAVITY = 1

PLAYER_SIZE = (32, 64)
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 10

ASSETS = Path('assets')
LEAVES = ASSETS / 'leaves'
GRASS = ASSETS / 'grass'
WOOD = ASSETS / 'wood'
PLAYER = ASSETS / 'player'
UI = ASSETS / 'ui'

TRANSPARENT_BLOCK = ASSETS / 'transparent_block.png'
SELECTION_BOX = UI / 'selection_box.png'
INVENTORY = UI / 'inventory.png'

BLOCKS = {
    'grass': str(GRASS / 'grass_2.png'),
    'oak_wood': str(WOOD / 'oak_wood.png'),
    'oak_leaves': str(LEAVES / 'oak_leaves.png')
}
