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
GRASS = ASSETS / 'grass'
PLAYER = ASSETS / 'player'
UI = ASSETS / 'ui'

TRANSPARENT_BLOCK = ASSETS / 'transparent_block.png'
SELECTION_BOX = UI / 'selection_box.png'
INVENTORY = UI / 'inventory.png'
