from pathlib import Path

import toml


CONFIG = toml.load('config.toml')

TITLE = CONFIG['title']
WINDOW_SIZE = (
    CONFIG['window_size']['x'],
    CONFIG['window_size']['y']
)
SCALING = CONFIG['scaling']

TILE_SIZE = 32
PLAYER_SIZE = (32, 64)

ASSETS = Path('assets')
GRASS = ASSETS / 'grass'
PLAYER = ASSETS / 'player'
