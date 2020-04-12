import arcade

from mc2d.config import (
    INVENTORY,
    MAX_STACK_SIZE,
    SCALING,
    SELECTION_BOX,
    TILE_SIZE,
    WINDOW_SIZE
)
from mc2d.utils import Block


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
        self.selected_item = None

    def setup(self):
        for i in range(5):
            sprite = Block(
                filename=str(SELECTION_BOX),
                scale=SCALING,
                center_x=self.center_x,
                center_y=self.top + 12 - int(TILE_SIZE * SCALING * (i + 1)) - (i * 13),
                name='transparent_block',
                amount=0
            )
            self.inv_sprites.append(sprite)

            amt_sprite = arcade.draw_text(
                str(sprite.amount),
                sprite.center_x + int(TILE_SIZE * SCALING) - (24 * SCALING),
                sprite.center_y - int(TILE_SIZE * SCALING) + (24 * SCALING),
                arcade.color.WHITE,
                font_size=10 * SCALING + i * 0.01,  # weird arcade cache.. uses the same instance
                bold=True                           # https://arcade.academy/_modules/arcade/text.html#draw_text
            )
            amt_sprite.alpha = 0
            self.block_amounts.append(amt_sprite)

        self.selected_item = arcade.Sprite(
            str(SELECTION_BOX),
            scale=SCALING,
            center_x=self.center_x,
            center_y=self.top + 12 - int(TILE_SIZE * SCALING * 1)
        )
        self.selected_item.index = 0

    def draw(self):
        super().draw()
        self.inv_sprites.draw()
        self.block_amounts.draw()
        self.selected_item.draw()

    def select_item(self, x, y, button, **viewport):
        x += viewport['left']
        y += viewport['bottom']

        if (
            self.left < x < self.right and
            self.bottom < y < self.top
        ):
            for idx, block in enumerate(self.inv_sprites):
                if (
                    block.left < x < block.right and
                    block.bottom < y < block.top
                ):
                    self.selected_item.index = idx
                    break

            return True
        return False

    def update_items(self, state, block=None):
        if state == 'ADD':
            for idx, inv_block in enumerate(self.inv_sprites):
                if inv_block.name == block.name and inv_block.name != 'transparent_block':
                    if inv_block.amount < MAX_STACK_SIZE:
                        inv_block.amount += 1

                        self.block_amounts.pop(idx)
                        self.block_amounts.insert(idx, arcade.draw_text(
                            str(inv_block.amount),
                            inv_block.center_x + int(TILE_SIZE * SCALING) - (24 * SCALING),
                            inv_block.center_y - int(TILE_SIZE * SCALING) + (24 * SCALING),
                            arcade.color.WHITE,
                            font_size=10 * SCALING + idx * 0.01,
                            bold=True
                        ))

                        return True

            for idx, inv_block in enumerate(self.inv_sprites):
                if inv_block.name == 'transparent_block':
                    block.center_x = self.center_x
                    block.center_y = self.top + 12 - int(TILE_SIZE * SCALING * (idx + 1)) - (idx * 13)

                    block.amount = 1
                    self.inv_sprites.pop(idx)
                    self.inv_sprites.insert(idx, block)

                    self.block_amounts.pop(idx)
                    self.block_amounts.insert(idx, arcade.draw_text(
                        str(block.amount),
                        inv_block.center_x + int(TILE_SIZE * SCALING) - (24 * SCALING),
                        inv_block.center_y - int(TILE_SIZE * SCALING) + (24 * SCALING),
                        arcade.color.WHITE,
                        font_size=10 * SCALING + idx * 0.01,
                        bold=True
                    ))

                    return True

            return False

        elif state == 'REMOVE':
            idx = self.selected_item.index
            inv_block = self.inv_sprites[idx]

            if inv_block.name != 'transparent_block':
                inv_block.amount -= 1

                self.block_amounts.pop(idx)
                amt_sprite = arcade.draw_text(
                    str(inv_block.amount),
                    inv_block.center_x + int(TILE_SIZE * SCALING) - (24 * SCALING),
                    inv_block.center_y - int(TILE_SIZE * SCALING) + (24 * SCALING),
                    arcade.color.WHITE,
                    font_size=10 * SCALING + idx * 0.01,
                    bold=True
                )

                if inv_block.amount == 0:
                    sprite = Block(
                        filename=str(SELECTION_BOX),
                        scale=SCALING,
                        center_x=self.center_x,
                        center_y=self.top + 12 - int(TILE_SIZE * SCALING * (idx + 1)) - (idx * 13),
                        name='transparent_block',
                        amount=0
                    )
                    self.inv_sprites.pop(idx)
                    self.inv_sprites.insert(idx, sprite)

                    amt_sprite.alpha = 0

                self.block_amounts.insert(idx, amt_sprite)

                return inv_block.name

            return False

    def update_view(self, **viewport):
        self.center_x = viewport['right'] - 48
        self.center_y = viewport['top'] - WINDOW_SIZE[1] // 2 + TILE_SIZE * SCALING

        for idx, sprite in enumerate(zip(self.inv_sprites, self.block_amounts)):
            sprite, amount = sprite
            sprite.center_x = self.center_x
            sprite.center_y = self.top + 12 - int(TILE_SIZE * SCALING * (idx + 1)) - (idx * 13)

            amount.center_x = sprite.center_x + int(TILE_SIZE * SCALING) - (24 * SCALING)
            amount.center_y = sprite.center_y - int(TILE_SIZE * SCALING) + (24 * SCALING)

            if self.selected_item.index == idx:
                self.selected_item.center_x = self.center_x
                self.selected_item.center_y = self.top + 12 - int(TILE_SIZE * SCALING * (idx + 1)) - (idx * 13)
