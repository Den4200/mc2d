import arcade

from mc2d.config import (
    SELECTION_BOX,
    SCALING,
    TILE_SIZE,
    WINDOW_SIZE
)


class Grid:

    def __init__(self):
        self.selection = None
        self.boxes = arcade.SpriteList()

    def draw(self):
        self.boxes.draw()

    def setup(self):
        pass

    def update(self, **viewport):
        if self.selection is not None:
            self.boxes.append(
                arcade.Sprite(
                    str(SELECTION_BOX),
                    scale=SCALING,
                    center_x=self.selection[0] + viewport['left'],
                    center_y=self.selection[1] + viewport['bottom']
                )
            )
            self.selection = None

            if len(self.boxes) > 1:
                self.boxes.pop(0)
