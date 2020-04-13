import arcade

from mc2d.config import (
    GRAVITY,
    VIEWPORT,
    WINDOW_SIZE
)
from mc2d.core import (
    Grid,
    Inventory,
    Player,
    World
)


class Mc2d(arcade.View):

    def __init__(self, menu, **kwargs) -> None:
        super().__init__()

        self.menu = menu

        self.world = None
        self.grid = None

        self.player = None
        self.inventory = None

        self.physics_engine = None

        self.view_bottom = kwargs.get('view_bottom', 0)
        self.view_left = kwargs.get('view_left', 0)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.world = World(self)
        self.world.setup()

        self.grid = Grid(self)
        self.grid.setup()

        self.inventory = Inventory(self)
        self.inventory.setup()

        self.player = Player(self)
        self.player.setup()

        self.post_setup()

    def post_setup(self):
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.world.block_list, GRAVITY
        )

    def on_draw(self):
        arcade.start_render()

        self.world.draw()
        self.grid.draw()

        self.inventory.draw()
        self.player.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button in (arcade.MOUSE_BUTTON_LEFT, arcade.MOUSE_BUTTON_RIGHT):
            self.grid.selection = (x, y, button)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.menu.save(
                mc2d=self,
                map_generator=self.world.map_generator,
                grid=self.grid,
                inventory=self.inventory,
                player=self.player,
                world=self.world
            )

            arcade.set_viewport(
                0,
                WINDOW_SIZE[0],
                0,
                WINDOW_SIZE[1]
            )

            self.window.show_view(self.menu)
            self.menu.setup()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.inventory.update()
        self.player.update()

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

        self.inventory.update_view(
            left=self.view_left,
            right=WINDOW_SIZE[0] + self.view_left,
            bottom=self.view_bottom,
            top=WINDOW_SIZE[1] + self.view_bottom
        )

        self.grid.update(
            left=self.view_left,
            right=WINDOW_SIZE[0] + self.view_left,
            bottom=self.view_bottom,
            top=WINDOW_SIZE[1] + self.view_bottom
        )
