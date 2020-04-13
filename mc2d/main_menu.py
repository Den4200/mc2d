import arcade

from mc2d.config import (
    MAIN_MENU_BG,
    PLAY_BUTTON_PRESSED,
    PLAY_BUTTON_RELEASED,
    WINDOW_SIZE
)
from mc2d.mc2d import Mc2d


class PlayButton(arcade.gui.TextButton):

    def __init__(self, ctx, x, y, width, height, theme=None):
        super().__init__(x, y, width, height, '', theme=theme)
        self.ctx = ctx
        self.pressed = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.ctx.play()
            self.pressed = False


class MainMenu(arcade.View):

    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture(
            str(MAIN_MENU_BG)
        )
        self.theme = None
        self.play_button = None

    def setup(self):
        self.theme = arcade.gui.Theme()
        self.theme.add_button_textures(
            normal=PLAY_BUTTON_RELEASED,
            clicked=PLAY_BUTTON_PRESSED
        )

        self.play_button = PlayButton(
            ctx=self,
            x=WINDOW_SIZE[0] / 2,
            y=WINDOW_SIZE[1] / 2,
            width=360,
            height=120,
            theme=self.theme
        )

        self.window.button_list.append(self.play_button)

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x=0,
            bottom_left_y=0,
            width=WINDOW_SIZE[0],
            height=WINDOW_SIZE[1],
            texture=self.background
        )

    def play(self):
        self.window.button_list.remove(self.play_button)
        self.window.show_view(Mc2d(self))
