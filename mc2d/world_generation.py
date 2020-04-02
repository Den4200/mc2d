import arcade

from mc2d.config import (
    GRASS,
    SELECTION_BOX,
    SCALING,
    TILE_SIZE,
    WINDOW_SIZE
)


class World:

    def __init__(self, ctx):
        self.ctx = ctx
        self.ground_idxs = [1, 2, 3]
        self.ground_list = arcade.SpriteList()
        self.grid_alphas = [
            [
                0 for _ in range(0, WINDOW_SIZE[0], int(TILE_SIZE * SCALING))
            ] for _ in range(0, WINDOW_SIZE[1], int(TILE_SIZE * SCALING))
        ]
        self.box_chosen_coords = None
        self.boxes = arcade.SpriteList()

    def setup(self):
        sprite = arcade.Sprite(
            str(GRASS / 'grass_1.png'),
            scale=SCALING,
            center_x=0,
            center_y=TILE_SIZE * SCALING // 2
        )
        sprite._cycle_idx = 1
        self.ground_list.append(sprite)

    def draw(self):
        self.ground_list.draw()
        self.boxes.draw()

    def update(self, **viewport):
        if self.box_chosen_coords is not None:
            self.boxes.append(
                arcade.Sprite(
                    str(SELECTION_BOX),
                    scale=SCALING,
                    center_x=self.box_chosen_coords[0] + viewport['left'],
                    center_y=self.box_chosen_coords[1] + viewport['bottom']
                )
            )
            self.box_chosen_coords = None

            if len(self.boxes) > 1:
                self.boxes.pop(0)

        if self.ground_list[0].left > viewport['left']:
            idx = self.ground_idxs[self.ground_list[0]._cycle_idx - 2]
            sprite = arcade.Sprite(
                str(GRASS / f'grass_{idx}.png'),
                scale=SCALING,
                center_x=self.ground_list[0].center_x - TILE_SIZE * SCALING,
                center_y=TILE_SIZE * SCALING // 2
            )
            sprite._cycle_idx = idx
            self.ground_list.insert(0, sprite)

        elif self.ground_list[-1].right < viewport['right']:
            idx = self.ground_idxs[self.ground_list[-1]._cycle_idx % 3]
            sprite = arcade.Sprite(
                str(GRASS / f'grass_{idx}.png'),
                scale=SCALING,
                center_x=self.ground_list[-1].center_x + TILE_SIZE * SCALING,
                center_y=TILE_SIZE * SCALING // 2
            )
            sprite._cycle_idx = idx
            self.ground_list.append(sprite)

        if self.ground_list[0].left + TILE_SIZE * SCALING < viewport['left']:
            self.ground_list.pop(0)

        elif self.ground_list[-1].right - TILE_SIZE * SCALING > viewport['right']:
            self.ground_list.pop(-1)
