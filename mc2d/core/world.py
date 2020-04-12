import arcade

from mc2d.config import (
    BLOCK_PATHS,
    CHUNK_SIZE,
    SCALING,
    TILE_SIZE
)
from mc2d.core.generators import MapGenerator
from mc2d.utils import Block


class World:

    def __init__(self, ctx):
        self.ctx = ctx
        self.block_list = arcade.SpriteList()

        self.map_generator = MapGenerator(ctx, *CHUNK_SIZE)

    def setup(self):
        self.map_generator.setup()

    def draw(self):
        self.block_list.draw()

    def is_block_here(self, center_x, center_y):
        for block in self.block_list:
            if block.center_x == center_x and block.center_y == center_y:
                return True

        return False

    def change_block(self, center_x, center_y, button, **viewport):
        if button == arcade.MOUSE_BUTTON_LEFT:

            for block in self.block_list:
                if block.center_x == center_x and block.center_y == center_y:

                    if self.ctx.inventory.update_items('ADD', block):
                        self.block_list.remove(block)

                    break

        elif button == arcade.MOUSE_BUTTON_RIGHT:

            for block in self.block_list:
                if block.center_x == center_x and block.center_y == center_y:
                    return

            sprite_name = self.ctx.inventory.update_items('REMOVE')
            if sprite_name and sprite_name != 'transparent_block':
                sprite = Block(
                    filename=BLOCK_PATHS[sprite_name],
                    scale=SCALING,
                    center_x=center_x,
                    center_y=center_y,
                    name=sprite_name
                )
                self.block_list.append(sprite)

    def update(self, **viewport):
        top_left_x = self.map_generator.chunk_pos_x
        chunk_size = int(TILE_SIZE * SCALING) * CHUNK_SIZE[0]

        if top_left_x[0] > viewport['left']:
            self.map_generator.generate_chunk('left')

        elif top_left_x[-1] + chunk_size < viewport['right']:
            self.map_generator.generate_chunk('right')
