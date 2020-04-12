import random

from mc2d.config import (
    BLOCK_IDS,
    BLOCK_PATHS,
    SCALING,
    TILE_SIZE,
    TREE_SHAPES
)
from mc2d.utils import Block


class MapGenerator:

    def __init__(self, ctx, chunk_size_x, chunk_size_y):
        self.ctx = ctx

        self.chunk_size_x = chunk_size_x
        self.chunk_size_y = chunk_size_y

        self.chunks = list()
        self.chunk_pos_x = list()

        self.DIRT_ID = 1
        self.GRASS_ID = 2

    def setup(self):
        self.generate_chunk('right')

    def generate_chunk(self, side):
        chunk = [[0 for _ in range(self.chunk_size_x)] for i in range(self.chunk_size_y)]

        # Set the bottom floor
        for y in range(1, self.chunk_size_y // 2):
            for x in range(self.chunk_size_x):
                chunk[-y][x] = 1

        layer_size = self.chunk_size_x
        for y in range(self.chunk_size_y - 1):
            if layer_size == 0:
                break

            layer_size = random.randrange(0, layer_size)
            layer_left_pos = random.randint(0, self.chunk_size_x - layer_size)

            for x in range(layer_size):

                # Check if a block is underneath
                if chunk[y - 1][x + layer_left_pos] == self.DIRT_ID:

                    # Check to see if the block is not on the edges
                    if layer_left_pos + x < self.chunk_size_x - 1 and layer_left_pos + x != 0:

                        # Check if there is a block diagonally down left and right
                        if (
                            chunk[y - 1][x + layer_left_pos - 1] == self.DIRT_ID and
                            chunk[y - 1][x + layer_left_pos + 1] == self.DIRT_ID
                        ):
                            chunk[y][x + layer_left_pos] = self.DIRT_ID

        chunk[:-(self.chunk_size_y // 2) + 1] = list(reversed(chunk[:-(self.chunk_size_y // 2) + 1]))
        chunk = self._treeify(self._grassify(chunk))

        if side == 'left':
            self.chunks.insert(0, chunk)
        elif side == 'right':
            self.chunks.append(chunk)

        self._blockify(chunk, side)

    def _blockify(self, chunk, side):
        if self.chunk_pos_x:
            if side == 'left':
                offset_x = self.chunk_pos_x[0] - int(TILE_SIZE * SCALING) * self.chunk_size_x
            elif side == 'right':
                offset_x = self.chunk_pos_x[-1] + int(TILE_SIZE * SCALING) * self.chunk_size_x
        else:
            offset_x = 0

        for y in range(self.chunk_size_y):
            for x in range(self.chunk_size_x):

                if chunk[y][x] == 0:
                    continue

                self.ctx.world.block_list.append(
                    Block(
                        scale=SCALING,
                        filename=BLOCK_PATHS[BLOCK_IDS[chunk[y][x]]],
                        center_x=x * int(TILE_SIZE * SCALING) + int(TILE_SIZE * SCALING) // 2 + offset_x,
                        center_y=(self.chunk_size_y - y) * int(TILE_SIZE * SCALING) + int(TILE_SIZE * SCALING) // 2,
                        name=BLOCK_IDS[chunk[y][x]]
                    )
                )

        if side == 'left':
            self.chunk_pos_x.insert(0, offset_x)
        elif side == 'right':
            self.chunk_pos_x.append(offset_x)

    def _grassify(self, chunk):
        grass_count = 0

        for y in range(self.chunk_size_y):
            for x in range(self.chunk_size_x):

                if grass_count == self.chunk_size_x:
                    return chunk

                if chunk[y][x] != 0:

                    # Check to make sure there is not grass or dirt above
                    if y == 0 or chunk[y - 1][x] not in (self.DIRT_ID, self.GRASS_ID):
                        chunk[y][x] = self.GRASS_ID
                        grass_count += 1

    def _treeify(self, chunk):
        _space = self.chunk_size_x // 8
        tree_amount = random.randrange(0, _space)
        spacing = 0

        for i in range(tree_amount):
            tree_shape = random.choice(TREE_SHAPES)

            min_spacing = 4
            max_spacing = tree_amount * _space
            if max_spacing == 4:
                max_spacing += 1

            spacing += random.randint(min_spacing, max_spacing)

            tree_y = self.chunk_size_y - 1
            while True:

                # Raise the tree until it's not in the ground
                if chunk[tree_y][spacing] != 0:
                    tree_y -= 1
                else:
                    break

            for y, _ in enumerate(tree_shape):
                for x, _ in enumerate(tree_shape[y]):

                    # Empty space
                    if tree_shape[y][x] == 0:
                        continue

                    chunk[tree_y - (len(tree_shape) - y - 1)][spacing + x - 3] = tree_shape[y][x]

                    # Make the blocks underneath the tree dirt
                    if y == len(tree_shape) - 1 and tree_shape[-1][x] != 0:
                        chunk[tree_y - (len(tree_shape) - y - 2)][spacing + x - 3] = self.DIRT_ID

        return chunk
