import json
import random

import arcade

from mc2d.config import (
    BLOCK_IDS,
    BLOCK_PATHS,
    GRASS,
    SCALING,
    TILE_SIZE,
    TREE_SHAPES
)


class Block(arcade.Sprite):

    def __init__(self, name, amount=1, cycle_idx=0, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.amount = amount
        self.cycle_idx = cycle_idx


class World:

    def __init__(self, ctx):
        self.ctx = ctx
        self.ground_idxs = [*range(1, 4)]
        self.ground_list = list()
        self.block_list = arcade.SpriteList()

        self.tree_generator = TreeGenerator(ctx)

    def setup(self):
        sprite = Block(
            filename=str(GRASS / 'grass_1.png'),
            scale=SCALING,
            center_x=TILE_SIZE * SCALING // 2,
            center_y=TILE_SIZE * SCALING // 2,
            name='grass',
            cycle_idx=1
        )
        self.ground_list.append(sprite)
        self.block_list.append(sprite)

        self.tree_generator.setup()

    def draw(self):
        self.block_list.draw()

    def is_block_here(self, center_x, center_y):
        for block in self.block_list:
            if block.center_x == center_x and block.center_y == center_y:
                return True

        return False

    def change_block(self, center_x, center_y, button, **viewport):
        if button == arcade.MOUSE_BUTTON_LEFT:

            for block in self.block_list:
                if block.center_x == center_x and block.center_y == center_y:

                    if self.ctx.inventory.update_items('ADD', block):
                        self.block_list.remove(block)

                    break

        elif button == arcade.MOUSE_BUTTON_RIGHT:

            for block in self.block_list:
                if block.center_x == center_x and block.center_y == center_y:
                    return

            sprite_name = self.ctx.inventory.update_items('REMOVE')
            if sprite_name and sprite_name != 'transparent_block':
                sprite = Block(
                    filename=BLOCK_PATHS[sprite_name],
                    scale=SCALING,
                    center_x=center_x,
                    center_y=center_y,
                    name=sprite_name
                )
                self.block_list.append(sprite)

    def update(self, **viewport):
        if self.ground_list[0].left > viewport['left']:
            idx = self.ground_idxs[self.ground_list[0].cycle_idx - 2]
            sprite = Block(
                filename=str(GRASS / f'grass_{idx}.png'),
                scale=SCALING,
                center_x=self.ground_list[0].center_x - int(TILE_SIZE * SCALING),
                center_y=int(TILE_SIZE * SCALING) // 2,
                name='grass',
                cycle_idx=idx
            )
            self.ground_list.insert(0, sprite)
            self.block_list.append(sprite)

            self.tree_generator.update('left')

        elif self.ground_list[-1].right < viewport['right']:
            idx = self.ground_idxs[self.ground_list[-1].cycle_idx % 3]
            sprite = Block(
                filename=str(GRASS / f'grass_{idx}.png'),
                scale=SCALING,
                center_x=self.ground_list[-1].center_x + int(TILE_SIZE * SCALING),
                center_y=int(TILE_SIZE * SCALING) // 2,
                name='grass',
                cycle_idx=idx
            )
            self.ground_list.append(sprite)
            self.block_list.append(sprite)

            self.tree_generator.update('right')

        if self.ground_list[0].left + int(TILE_SIZE * SCALING) < viewport['left']:
            self.block_list.remove(self.ground_list.pop(0))

        elif self.ground_list[-1].right - int(TILE_SIZE * SCALING) > viewport['right']:
            self.block_list.remove(self.ground_list.pop(-1))


class TreeGenerator:

    def __init__(self, ctx):
        self.ctx = ctx
        self.trees = list()
        self.tree_distance = None

    def setup(self):
        self._generate_random_distance()
        self.one(5, 0, 0)

    def _generate_random_distance(self):
        if self.tree_distance is None:
            self.tree_distance = random.randrange(16, 41, 8)

    def one(self, offset_x_blocks, offset_y_blocks, idx):
        tree_shape = random.choice(
            json.loads(TREE_SHAPES.read_text())
        )
        if self.trees:
            offset_x = offset_x_blocks * int(TILE_SIZE * SCALING) + self.trees[idx][0]
            offset_y = offset_y_blocks * int(TILE_SIZE * SCALING) + self.trees[idx][1]
        else:
            offset_x = offset_x_blocks * int(TILE_SIZE * SCALING) + int(TILE_SIZE * SCALING) // 2
            offset_y = offset_y_blocks * int(TILE_SIZE * SCALING) + int(TILE_SIZE * SCALING) // 2

        self.ctx.world.block_list.extend((
            Block(
                scale=SCALING,
                name=BLOCK_IDS[tree_shape[y][x]],
                filename=BLOCK_PATHS[BLOCK_IDS[tree_shape[y][x]]],
                center_x=x * int(TILE_SIZE * SCALING) + offset_x,
                center_y=(len(tree_shape) - y) * int(TILE_SIZE * SCALING) + offset_y
            ) for x in range(len(tree_shape[0])) for y in range(len(tree_shape)) if tree_shape[y][x] != 0
        ))

        base_tree_pos = (
            (len(tree_shape[0]) // 2 + 1) * int(TILE_SIZE * SCALING) + offset_x,
            offset_y
        )

        if idx == -1:
            self.trees.append(base_tree_pos)
        else:
            self.trees.insert(idx, base_tree_pos)

        print(len(self.trees))

    def update(self, direction):
        self._generate_random_distance()
        detect_range = 12 * int(TILE_SIZE * SCALING)

        if direction == 'left':
            if self.ctx.player.center_x < self.trees[0][0] + detect_range:
                self.one(-self.tree_distance, 0, 0)
                self.tree_distance = None

        elif direction == 'right':
            if self.trees[-1][0] - detect_range < self.ctx.player.center_x:
                self.one(self.tree_distance, 0, -1)
                self.tree_distance = None
