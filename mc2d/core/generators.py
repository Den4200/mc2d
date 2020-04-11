import random

from mc2d.config import (
    BLOCK_IDS,
    BLOCK_PATHS,
    SCALING,
    TILE_SIZE,
    TREE_SHAPES
)
from mc2d.utils import Block


class TreeGenerator:

    def __init__(self, ctx):
        self.ctx = ctx
        self.trees = list()
        self.tree_distance = None

    def setup(self):
        self._generate_random_distance()
        self.one(6, 0, 0)

    def _generate_random_distance(self):
        if self.tree_distance is None:
            self.tree_distance = random.randrange(16, 41, 8)

    def one(self, offset_x_blocks, offset_y_blocks, idx):
        tree_shape = random.choice(TREE_SHAPES)

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
        chunk = [[0 for _ in range(self.chunk_size_x)]for i in range(self.chunk_size_y)]

        # Set the bottom floor
        for y in range(1, 5):
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

        chunk[:-4] = list(reversed(chunk[:-4]))
        chunk = self._grassify(chunk)

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
        elif side =='right':
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
