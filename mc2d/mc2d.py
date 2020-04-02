import arcade

from mc2d.player import Player
from mc2d.grid import Grid
from mc2d.world_generation import World
from mc2d.config import (
    GRAVITY,
    PLAYER,
    PLAYER_JUMP_SPEED,
    PLAYER_MOVEMENT_SPEED,
    PLAYER_SIZE,
    SCALING,
    TILE_SIZE,
    TITLE,
    VIEWPORT,
    WINDOW_SIZE
)


class Mc2d(arcade.Window):

    def __init__(self) -> None:
        super().__init__(*WINDOW_SIZE, TITLE)

        self.world = None
        self.grid = None
        self.player = None

        self.physics_engine = None

        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.player = Player(
            str(PLAYER / 'idle.png'),
            scale=SCALING,
            center_x=PLAYER_SIZE[0] * SCALING,
            center_y=PLAYER_SIZE[1] * SCALING // 2 + TILE_SIZE * SCALING
        )

        self.world = World()
        self.world.setup()

        self.grid = Grid()
        self.grid.setup()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.world.ground_list, GRAVITY
        )

    def on_draw(self):
        arcade.start_render()

        self.player.draw()
        self.world.draw()
        self.grid.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.physics_engine.can_jump():
            self.player.change_y = PLAYER_JUMP_SPEED

        if key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED

        if key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.grid.selection = (x, y)

    def on_update(self, delta_time):
        self.physics_engine.update()

        changed = False

        left_boundary = self.view_left + VIEWPORT['left']
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        right_boundary = self.view_left + WINDOW_SIZE[0] - VIEWPORT['right']
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + WINDOW_SIZE[1] - VIEWPORT['top']
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + VIEWPORT['bottom']
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            self.world.update(
                left=self.view_left,
                right=WINDOW_SIZE[0] + self.view_left,
                bottom=self.view_bottom,
                top=WINDOW_SIZE[1] + self.view_bottom
            )

            arcade.set_viewport(
                self.view_left,
                WINDOW_SIZE[0] + self.view_left,
                self.view_bottom,
                WINDOW_SIZE[1] + self.view_bottom
            )

        self.grid.update(
            left=self.view_left,
            right=WINDOW_SIZE[0] + self.view_left,
            bottom=self.view_bottom,
            top=WINDOW_SIZE[1] + self.view_bottom
        )
