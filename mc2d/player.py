import arcade

from mc2d.config import (
    PLAYER_JUMP_SPEED,
    PLAYER_MOVEMENT_SPEED,
    SCALING,
    TILE_SIZE
)
from mc2d.utils import find_grid_box


class Player(arcade.Sprite):

    def __init__(self, ctx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.destination = None
        self.button = None

        self.prev_coords = None

    def update(self):
        if self.destination is not None and self.button is not None:
            half_tile = int(TILE_SIZE * SCALING) // 2

            if self.prev_coords is not None:
                prev_x, prev_y = find_grid_box(*self.prev_coords)

                if self.center_x == self.prev_coords[0] and self.center_y == self.prev_coords[1]:

                    if self.ctx.physics_engine.can_jump():
                        self.change_y = PLAYER_JUMP_SPEED
                        self.path_attempted = True
                        self.is_jumping = True
                    else:
                        self.reset()

            if self.destination is not None:

                if (
                    self.destination[0] - half_tile < self.center_x < self.destination[0] + half_tile
                    and
                    self.destination[1] - half_tile < self.center_y < self.destination[1] + half_tile
                ):
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
        self.ctx.grid.selection = (*self.destination[3:], self.button)

        self.button = None
        self.destination = None
        self.prev_coords = None
