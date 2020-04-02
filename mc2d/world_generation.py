import arcade

from mc2d.config import (
    GRASS,
    SCALING,
    TILE_SIZE
)


class World:

    def __init__(self, ctx):
        self.ctx = ctx
        self.ground_idxs = [1, 2, 3]
        self.ground_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList()

    def setup(self):
        sprite = arcade.Sprite(
            str(GRASS / 'grass_1.png'),
            scale=SCALING,
            center_x=0,
            center_y=TILE_SIZE * SCALING // 2
        )
        sprite._cycle_idx = 1
        self.ground_list.append(sprite)
        self.block_list.append(sprite)

    def draw(self):
        self.block_list.draw()

    def check_block(self, left_x, bottom_y, button):
        for block in self.block_list:
            if (
                left_x < block.center_x < left_x + int(TILE_SIZE * SCALING) and
                bottom_y < block.center_y < bottom_y + int(TILE_SIZE * SCALING)
            ):
                return

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.block_list.append(
                arcade.Sprite(
                    str(GRASS / 'grass_2.png'),  # placeholder until inventory system
                    scale=SCALING,
                    center_x=left_x + (TILE_SIZE * SCALING) // 2,
                    center_y=bottom_y + (TILE_SIZE * SCALING) // 2
                )
            )

    def update(self, **viewport):
        if self.ground_list[0].left > viewport['left']:
            idx = self.ground_idxs[self.ground_list[0]._cycle_idx - 2]
            sprite = arcade.Sprite(
                str(GRASS / f'grass_{idx}.png'),
                scale=SCALING,
                center_x=self.ground_list[0].center_x - int(TILE_SIZE * SCALING),
                center_y=int(TILE_SIZE * SCALING) // 2
            )
            sprite._cycle_idx = idx
            self.ground_list.insert(0, sprite)
            self.block_list.append(sprite)

        elif self.ground_list[-1].right < viewport['right']:
            idx = self.ground_idxs[self.ground_list[-1]._cycle_idx % 3]
            sprite = arcade.Sprite(
                str(GRASS / f'grass_{idx}.png'),
                scale=SCALING,
                center_x=self.ground_list[-1].center_x + int(TILE_SIZE * SCALING),
                center_y=int(TILE_SIZE * SCALING) // 2
            )
            sprite._cycle_idx = idx
            self.ground_list.append(sprite)
            self.block_list.append(sprite)

        if self.ground_list[0].left + int(TILE_SIZE * SCALING) < viewport['left']:
            self.block_list.remove(self.ground_list.pop(0))

        elif self.ground_list[-1].right - int(TILE_SIZE * SCALING) > viewport['right']:
            self.block_list.remove(self.ground_list.pop(-1))
