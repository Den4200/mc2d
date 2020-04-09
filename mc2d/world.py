import arcade

from mc2d.config import (
    BLOCKS,
    GRASS,
    SCALING,
    TILE_SIZE
)


class World:

    def __init__(self, ctx):
        self.ctx = ctx
        self.ground_idxs = [*range(1, 4)]
        self.ground_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList()

    def setup(self):
        sprite = arcade.Sprite(
            str(GRASS / 'grass_1.png'),
            scale=SCALING,
            center_x=0,
            center_y=TILE_SIZE * SCALING // 2
        )
        sprite.name = 'grass'
        sprite._cycle_idx = 1
        self.ground_list.append(sprite)
        self.block_list.append(sprite)

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

                    if self.ctx.inventory.update_items(block, 'ADD'):
                        self.block_list.remove(block)

                    break

        elif button == arcade.MOUSE_BUTTON_RIGHT:

            for block in self.block_list:
                if (block.center_x == center_x and block.center_y == center_y):
                    return

            if self.ctx.inventory.update_items(block, 'REMOVE'):
                sprite_name = self.ctx.inventory.inv_sprites[self.ctx.inventory.selected_item.index].name

                if sprite_name != 'transparent_block':
                    sprite = arcade.Sprite(
                        BLOCKS[sprite_name],
                        scale=SCALING,
                        center_x=center_x,
                        center_y=center_y
                    )
                    sprite.name = sprite_name
                    self.block_list.append(sprite)

    def update(self, **viewport):
        if self.ground_list[0].left > viewport['left']:
            idx = self.ground_idxs[self.ground_list[0]._cycle_idx - 2]
            sprite = arcade.Sprite(
                str(GRASS / f'grass_{idx}.png'),
                scale=SCALING,
                center_x=self.ground_list[0].center_x - int(TILE_SIZE * SCALING),
                center_y=int(TILE_SIZE * SCALING) // 2
            )
            sprite.name = 'grass'
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
            sprite.name = 'grass'
            sprite._cycle_idx = idx
            self.ground_list.append(sprite)
            self.block_list.append(sprite)

        if self.ground_list[0].left + int(TILE_SIZE * SCALING) < viewport['left']:
            self.block_list.remove(self.ground_list.pop(0))

        elif self.ground_list[-1].right - int(TILE_SIZE * SCALING) > viewport['right']:
            self.block_list.remove(self.ground_list.pop(-1))
