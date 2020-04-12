import arcade

from mc2d.config import SCALING, TILE_SIZE


class Block(arcade.Sprite):

    def __init__(self, name, amount=1, cycle_idx=0, **kwargs):
        super().__init__(**kwargs)

        self.name = name
        self.amount = amount
        self.cycle_idx = cycle_idx


def find_grid_box(x, y):
    left_x = x - (x % int(TILE_SIZE * SCALING))
    bottom_y = y - (y % int(TILE_SIZE * SCALING))

    center_x = left_x + int(TILE_SIZE * SCALING) // 2
    center_y = bottom_y + int(TILE_SIZE * SCALING) // 2

    return center_x, center_y
