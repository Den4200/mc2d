import arcade

from mc2d.config import (
    LOAD_WORLD_BUTTON_PRESSED,
    LOAD_WORLD_BUTTON_RELEASED,
    MAIN_MENU_BG,
    NEW_WORLD_BUTTON_PRESSED,
    NEW_WORLD_BUTTON_RELEASED,
    WINDOW_SIZE
)
from mc2d.factory import Factory
from mc2d.mc2d import Mc2d


class NewWorldButton(arcade.gui.TextButton):

    def __init__(self, ctx, x, y, width, height, theme=None):
        super().__init__(x, y, width, height, '', theme=theme)
        self.ctx = ctx
        self.pressed = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.ctx.new_world()
            self.pressed = False


class LoadWorldButton(arcade.gui.TextButton):

    def __init__(self, ctx, x, y, width, height, theme=None):
        super().__init__(x, y, width, height, '', theme=theme)
        self.ctx = ctx
        self.pressed = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.ctx.load_world()
            self.pressed = False


class MainMenu(arcade.View):

    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture(
            str(MAIN_MENU_BG)
        )
        self.new_world_button = None
        self.load_world_button = None

    def setup(self):
        new_world_theme = arcade.gui.Theme()
        new_world_theme.add_button_textures(
            normal=NEW_WORLD_BUTTON_RELEASED,
            clicked=NEW_WORLD_BUTTON_PRESSED
        )

        load_world_theme = arcade.gui.Theme()
        load_world_theme.add_button_textures(
            normal=LOAD_WORLD_BUTTON_RELEASED,
            clicked=LOAD_WORLD_BUTTON_PRESSED
        )

        self.new_world_button = NewWorldButton(
            ctx=self,
            x=WINDOW_SIZE[0] / 2,
            y=WINDOW_SIZE[1] / 2 + 50,
            width=360,
            height=120,
            theme=new_world_theme
        )

        self.load_world_button = LoadWorldButton(
            ctx=self,
            x=WINDOW_SIZE[0] / 2,
            y=WINDOW_SIZE[1] / 2 - 100,
            width=360,
            height=120,
            theme=load_world_theme
        )

        self.window.button_list.append(self.new_world_button)
        self.window.button_list.append(self.load_world_button)

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x=0,
            bottom_left_y=0,
            width=WINDOW_SIZE[0],
            height=WINDOW_SIZE[1],
            texture=self.background
        )

    def new_world(self):
        self.window.button_list.remove(self.new_world_button)
        self.window.button_list.remove(self.load_world_button)

        mc2d = Mc2d(self)
        mc2d.setup()

        self.window.show_view(mc2d)

    def load_world(self):
        self.window.button_list.remove(self.new_world_button)
        self.window.button_list.remove(self.load_world_button)

        factory = Factory()
        with open('saves/test.json', 'r') as f:
            factory.load(f, self)

        factory.mc2d.post_setup()

        self.window.show_view(factory.mc2d)

    def save(self, **kwargs):
        factory = Factory(**kwargs)
        with open('saves/test.json', 'w') as f:
            factory.dump(f)
