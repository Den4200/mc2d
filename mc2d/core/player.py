import arcade

from mc2d.config import (
    PLAYER,
    PLAYER_JUMP_SPEED,
    PLAYER_MOVEMENT_SPEED,
    PLAYER_SIZE,
    SCALING,
    TILE_SIZE
)
from mc2d.utils import find_grid_box


class Player(arcade.Sprite):

    def __init__(self, ctx):
        super().__init__(
            str(PLAYER / 'idle.png'),
            scale=SCALING,
            center_x=PLAYER_SIZE[0] * SCALING,
            center_y=PLAYER_SIZE[1] * SCALING // 2 + TILE_SIZE * SCALING
        )
        self.ctx = ctx
        self.destination = None
        self.button = None

        self.MAX_ATTEMPTS = 12
        self.prev_coords = list()
        self.just_started = True

    def setup(self):
        pass

    def update(self):
        if self.destination is not None and self.button is not None:
            scaled_tile = int(TILE_SIZE * SCALING)
            half_tile = scaled_tile // 2

            if self.prev_coords:
                prev_attempts = [find_grid_box(*prev_coords) for prev_coords in self.prev_coords]

                if (
                    len(prev_attempts) == self.MAX_ATTEMPTS and
                    all(prev_attempts[0] == prev_attempt for prev_attempt in prev_attempts[1:])
                ):
                    self.reset()
                    return

                if self.center_x == self.prev_coords[-1][0] and self.center_y == self.prev_coords[-1][1]:

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
                return

            if self.destination[0] > self.center_x:
                self.change_x = PLAYER_MOVEMENT_SPEED
            else:
                self.change_x = -PLAYER_MOVEMENT_SPEED

            self.prev_coords.append((self.center_x, self.center_y))
            if len(self.prev_coords) > self.MAX_ATTEMPTS:
                self.prev_coords.pop(0)

    def reset(self):
        self.change_x = 0
        self.change_y = 0

        self.ctx.grid.should_not_check = True
        self.ctx.world.change_block(*self.destination[:2], self.button, **self.destination[-1])
        self.ctx.grid.selection = (*self.destination[3:-1], self.button)

        self.button = None
        self.destination = None
        self.prev_coords = list()
        self.just_started = True
