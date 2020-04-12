import arcade

from mc2d.config import (
    FULLSCREEN,
    TITLE,
    WINDOW_SIZE
)
from mc2d.main_menu import MainMenu


def main():
    window = arcade.Window(*WINDOW_SIZE, TITLE, fullscreen=FULLSCREEN)
    main_menu = MainMenu()

    window.show_view(main_menu)
    main_menu.setup()

    arcade.run()


if __name__ == "__main__":
    main()
