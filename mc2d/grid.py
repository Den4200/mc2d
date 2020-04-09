import arcade

from mc2d.config import SCALING, SELECTION_BOX
from mc2d.utils import find_grid_box


class Grid:

    def __init__(self, ctx):
        self.ctx = ctx
        self.selection = None
        self.should_not_check = False
        self.boxes = arcade.SpriteList()

    def draw(self):
        self.boxes.draw()

    def setup(self):
        pass

    def update(self, **viewport):
        if self.selection is not None:
            if not self.ctx.inventory.select_item(*self.selection, **viewport):

                center_x, center_y = find_grid_box(
                    self.selection[0] + viewport['left'],
                    self.selection[1] + viewport['bottom']
                )

                if len(self.boxes) > 0:
                    if self.boxes[0].center_x == center_x and self.boxes[0].center_y == center_y:
                        self.boxes.pop(0)
                        self.selection = None

                        self.ctx.player.button = None
                        self.ctx.player.destination = None
                        self.ctx.player.change_x = 0
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

                if not self.should_not_check:
                    self.ctx.player.destination = (center_x, center_y, *self.selection, viewport)
                    self.ctx.player.button = self.selection[2]
                else:
                    self.should_not_check = False

            self.selection = None
