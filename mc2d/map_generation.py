import arcade

from mc2d.config import (
    GRASS,
    SCALING,
    TILE_SIZE,
)


class Map:

    def __init__(self, ctx):
        self.ctx = ctx
        self.ground_idxs = [1, 2, 3]

    def setup(self):
        self.ctx.ground_list = arcade.SpriteList()

        sprite = arcade.Sprite(
            str(GRASS / 'grass_1.png'),
            scale=SCALING,
            center_x=0,
            center_y=TILE_SIZE * SCALING // 2
        )
        sprite._cycle_idx = 1
        self.ctx.ground_list.append(sprite)

    def update(self, **viewport):
        ground_list = self.ctx.ground_list

        if ground_list[0].left > viewport['left']:
            idx = self.ground_idxs[ground_list[0]._cycle_idx - 2]
            sprite = arcade.Sprite(
                str(GRASS / f'grass_{idx}.png'),
                scale=SCALING,
                center_x=ground_list[0].center_x - TILE_SIZE * SCALING,
                center_y=TILE_SIZE * SCALING // 2
            )
            sprite._cycle_idx = idx
            ground_list.insert(0, sprite)

        if ground_list[-1].right < viewport['right']:
            idx = self.ground_idxs[ground_list[-1]._cycle_idx % 3]
            sprite = arcade.Sprite(
                str(GRASS / f'grass_{idx}.png'),
                scale=SCALING,
                center_x=ground_list[-1].center_x + TILE_SIZE * SCALING,
                center_y=TILE_SIZE * SCALING // 2
            )
            sprite._cycle_idx = idx
            ground_list.append(sprite)
