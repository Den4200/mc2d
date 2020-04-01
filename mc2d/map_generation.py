import itertools

import arcade

from mc2d.config import (
    GRASS,
    SCALING,
    TILE_SIZE,
    WINDOW_SIZE
)


class Map:

    def __init__(self, ctx):
        self.ctx = ctx

    def setup(self):
        self.ctx.ground_list = arcade.SpriteList()

        ground_cycle = itertools.cycle(
            str(GRASS / f'grass_{i}.png') for i in range(1, 4)
        )

        for x in range(0, int((WINDOW_SIZE[0] + TILE_SIZE) / SCALING), TILE_SIZE):
            self.ctx.ground_list.append(
                arcade.Sprite(
                    next(ground_cycle),
                    scale=SCALING,
                    center_x=x * SCALING,
                    center_y=TILE_SIZE * SCALING // 2
                )
            )
