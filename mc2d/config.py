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

TILE_SIZE = 32

GRAVITY = 1

PLAYER_SIZE = (32, 64)
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 10

ASSETS = Path('assets')
GRASS = ASSETS / 'grass'
PLAYER = ASSETS / 'player'

SELECTION_BOX = ASSETS / 'selection_box.png'
