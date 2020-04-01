import itertools

import arcade

from mc2d.constants import (
    TITLE,
    SCREEN_SIZE,
    TILE_SIZE,
    SCALING,
    GRASS
)


class Mc2d(arcade.Window):

    def __init__(self) -> None:
        super().__init__(*SCREEN_SIZE, TITLE)

        self.ground_list = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.ground_list = arcade.SpriteList()

        ground_cycle = itertools.cycle(
            str(GRASS / f'grass_{i}.png') for i in range(1, 4)
        )

        for x in range(0, SCREEN_SIZE[0] + TILE_SIZE, TILE_SIZE):
            self.ground_list.append(
                arcade.Sprite(
                    next(ground_cycle),
                    scale=SCALING,
                    center_x=x * SCALING,
                    center_y=TILE_SIZE * SCALING // 2
                )
            )

    def on_draw(self):
        arcade.start_render()

        self.ground_list.draw()


def main():
    window = Mc2d()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
