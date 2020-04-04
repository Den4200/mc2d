import arcade

from mc2d.config import (
    GRASS,
    PLAYER_JUMP_SPEED,
    PLAYER_MOVEMENT_SPEED,
    SCALING,
    TILE_SIZE,
    SELECTION_BOX
)
from mc2d.utils import find_grid_box


class Player(arcade.Sprite):

    def __init__(self, ctx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.destination = None
        self.button = None

        self.prev_coords = None
        self.just_started = True

        self.inv_sprites = arcade.SpriteList()

    def setup(self):
        for i in range(4):
            sprite = arcade.Sprite(
                str(SELECTION_BOX),
                scale=SCALING,
                center_x=self.ctx.inventory_ui.center_x,
                center_y=self.ctx.inventory_ui.top + 8 + (TILE_SIZE * SCALING * (i + 1)) // 2
            )
            sprite.name = 'transparent_block'
            sprite.amount = 0
            self.inv_sprites.append(sprite)

        # here until more advanced map generation
        sprite = arcade.Sprite(
            str(GRASS),
            scale=SCALING,
            center_x=self.ctx.inventory_ui.center_x,
            center_y=self.ctx.inventory_ui.top + 8 + (TILE_SIZE * SCALING * 5) // 2
        )
        sprite.name = 'grass'
        sprite.amount = 32
        self.inv_sprites.append(sprite)

    def update_inventory(self, block, state):
        if state == 'ADD':
            for inv_block in self.inv_sprites:
                if inv_block.name == block.name and inv_block.name != 'transparent_block':
                    if inv_block.amount < 64:
                        inv_block.amount += 1
                        return True

            for idx, inv_block in enumerate(self.inv_sprites):
                if inv_block.name == 'transparent_block':
                    block.center_x = self.ctx.inventory_ui.center_x
                    block.center_y = self.ctx.inventory_ui.top + 8 + (TILE_SIZE * SCALING * (idx + 1)) // 2

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
                            center_x=self.ctx.inventory_ui.center_x,
                            center_y=self.ctx.inventory_ui.top + 8 + (TILE_SIZE * SCALING * (idx + 1)) // 2
                        )
                        sprite.name = 'transparent_block'
                        sprite.amount = 0
                        self.inv_sprites.pop(idx)
                        self.inv_sprites.insert(idx, sprite)

                    return True

            return False

    def update(self):
        print(*(f'{sprite.name}({sprite.amount})' for sprite in self.inv_sprites))
        if self.destination is not None and self.button is not None:
            scaled_tile = int(TILE_SIZE * SCALING)
            half_tile = scaled_tile // 2

            if self.prev_coords is not None:
                prev_x, prev_y = find_grid_box(*self.prev_coords)

                if self.center_x == self.prev_coords[0] and self.center_y == self.prev_coords[1]:

                    if self.ctx.physics_engine.can_jump() and not self.just_started:
                        self.change_y = PLAYER_JUMP_SPEED
                        self.is_jumping = True

                    elif self.just_started:
                        self.just_started = False

                    else:
                        self.reset()
                        return

            if self.ctx.world.is_block_here(*self.destination[:2]) or self.button == arcade.MOUSE_BUTTON_RIGHT:
                tile = scaled_tile
            else:
                tile = half_tile

            if all((
                self.destination[0] - tile < self.center_x < self.destination[0] + tile,
                self.destination[1] - tile < self.center_y < self.destination[1] + tile
            )):
                self.reset()

            else:
                if self.destination[0] > self.center_x:
                    self.change_x = PLAYER_MOVEMENT_SPEED
                else:
                    self.change_x = -PLAYER_MOVEMENT_SPEED

            self.prev_coords = (self.center_x, self.center_y)

    def reset(self):
        self.change_x = 0
        self.change_y = 0

        self.ctx.grid.should_not_check = True
        self.ctx.world.change_block(*self.destination[:2], self.button, **self.destination[-1])
        self.ctx.grid.selection = (*self.destination[3:-1], self.button)

        self.button = None
        self.destination = None
        self.prev_coords = None
        self.just_started = True
