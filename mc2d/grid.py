import arcade

from mc2d.config import (
    SELECTION_BOX,
    SCALING,
    TILE_SIZE
)


class Grid:

    def __init__(self, ctx):
        self.ctx = ctx
        self.selection = None
        self.boxes = arcade.SpriteList()

    def draw(self):
        self.boxes.draw()

    def setup(self):
        pass

    def update(self, **viewport):
        if self.selection is not None:
            center_x = self.selection[0] + viewport['left']
            center_y = self.selection[1] + viewport['bottom']

            left_x = center_x - (center_x % int(TILE_SIZE * SCALING))
            bottom_y = center_y - (center_y % int(TILE_SIZE * SCALING))

            center_x = left_x + (TILE_SIZE * SCALING) // 2
            center_y = bottom_y + (TILE_SIZE * SCALING) // 2

            if len(self.boxes) > 0:
                if self.boxes[0].center_x == center_x and self.boxes[0].center_y == center_y:
                    self.boxes.pop(0)
                    self.selection = None
                    return

            self.boxes.append(
                arcade.Sprite(
                    str(SELECTION_BOX),
                    scale=SCALING,
                    center_x=center_x,
                    center_y=center_y
                )
            )

            if len(self.boxes) > 1:
                self.boxes.pop(0)

            self.ctx.world.check_block(left_x, bottom_y, self.selection[2])
            self.selection = None
