import arcade

from mc2d.config import (
    GRASS,
    INVENTORY,
    MAX_STACK_SIZE,
    SCALING,
    SELECTION_BOX,
    TILE_SIZE,
    WINDOW_SIZE
)


class Inventory(arcade.Sprite):

    def __init__(self, ctx):
        super().__init__(
            str(INVENTORY),
            scale=SCALING,
            center_x=WINDOW_SIZE[0] - 24,
            center_y=WINDOW_SIZE[1] // 2
        )
        self.ctx = ctx

        self.inv_sprites = arcade.SpriteList()
        self.block_amounts = arcade.SpriteList()

    def setup(self):
        for i in range(4):
            sprite = arcade.Sprite(
                str(SELECTION_BOX),
                scale=SCALING,
                center_x=self.center_x,
                center_y=self.top + 12 - int(TILE_SIZE * SCALING * (i + 1)) - (i * 13)
            )
            sprite.name = 'transparent_block'
            sprite.amount = 0
            self.inv_sprites.append(sprite)
            self.block_amounts.append(
                arcade.draw_text(
                    str(sprite.amount),
                    sprite.center_x + int(TILE_SIZE * SCALING) - (23 * SCALING),
                    sprite.center_y - int(TILE_SIZE * SCALING) + (23 * SCALING),
                    arcade.color.WHITE,
                    font_size=10 * SCALING,
                    bold=True
                )
            )

        # here until more advanced map generation
        sprite = arcade.Sprite(
            str(GRASS / 'grass_2.png'),
            scale=SCALING,
            center_x=self.center_x,
            center_y=self.top + 12 - int(TILE_SIZE * SCALING * 5) - (4 * 13)
        )
        sprite.name = 'grass'
        sprite.amount = 8
        self.inv_sprites.append(sprite)
        self.block_amounts.append(
            arcade.draw_text(
                str(sprite.amount),
                sprite.center_x + int(TILE_SIZE * SCALING) - (23 * SCALING),
                sprite.center_y - int(TILE_SIZE * SCALING) + (23 * SCALING),
                arcade.color.WHITE,
                font_size=10 * SCALING,
                bold=True
            )
        )

    def draw(self):
        super().draw()
        self.inv_sprites.draw()
        self.block_amounts.draw()

    def update_items(self, block, state):
        if state == 'ADD':
            for inv_block in self.inv_sprites:
                if inv_block.name == block.name and inv_block.name != 'transparent_block':
                    if inv_block.amount < MAX_STACK_SIZE:
                        inv_block.amount += 1
                        return True

            for idx, inv_block in enumerate(self.inv_sprites):
                if inv_block.name == 'transparent_block':
                    block.center_x = self.center_x
                    block.center_y = self.top + 12 - int(TILE_SIZE * SCALING * (idx + 1)) - (idx * 13)

                    block.amount = 1
                    self.inv_sprites.pop(idx)
                    self.inv_sprites.insert(idx, block)
                    return True

            return False

        elif state == 'REMOVE':
            for idx, inv_block in enumerate(self.inv_sprites):
                if inv_block.name == block.name and inv_block.name != 'transparent_block':
                    inv_block.amount -= 1

                    if inv_block.amount == 0:
                        sprite = arcade.Sprite(
                            str(SELECTION_BOX),
                            scale=SCALING,
                            center_x=self.center_x,
                            center_y=self.top + 12 - int(TILE_SIZE * SCALING * (idx + 1)) - (idx * 13)
                        )
                        sprite.name = 'transparent_block'
                        sprite.amount = 0
                        self.inv_sprites.pop(idx)
                        self.inv_sprites.insert(idx, sprite)

                    return True

            return False

    def update_view(self, **viewport):
        print(*(f'{sprite.name}({sprite.amount})' for sprite in self.inv_sprites))

        self.center_x = viewport['right'] - 48
        self.center_y = viewport['top'] - WINDOW_SIZE[1] // 2 + TILE_SIZE * SCALING

        for idx, sprite in enumerate(zip(self.inv_sprites, self.block_amounts)):
            sprite, amount = sprite
            sprite.center_x = self.center_x
            sprite.center_y = self.top + 12 - int(TILE_SIZE * SCALING * (idx + 1)) - (idx * 13)

            amount.center_x = sprite.center_x + int(TILE_SIZE * SCALING) - (23 * SCALING)
            amount.center_y = sprite.center_y - int(TILE_SIZE * SCALING) + (23 * SCALING)
