import random

from mc2d.config import (
    BLOCK_IDS,
    BLOCK_PATHS,
    SCALING,
    TILE_SIZE,
    TREE_SHAPES
)
from mc2d.utils import find_grid_box, Block


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

    def find_chunk(self, x, y):
        chunk_top = self.chunk_size_y * int(TILE_SIZE * SCALING) + int(TILE_SIZE * SCALING) // 2
        chunk_bottom = int(TILE_SIZE * SCALING) + int(TILE_SIZE * SCALING) // 2

        for idx, chunk in enumerate(self.chunks):
            chunk_left = self.chunk_pos_x[idx]
            chunk_right = chunk_left + self.chunk_size_x * int(TILE_SIZE * SCALING)

            if chunk_left <= x <= chunk_right and chunk_bottom <= y <= chunk_top:
                print('find_chunk:', chunk_left, chunk_right, chunk_bottom, chunk_top)
                return {
                    'chunk': chunk,
                    'top': chunk_top,
                    'bottom': chunk_bottom,
                    'left': chunk_left,
                    'right': chunk_right,
                    'index': idx
                }

    def find_chunk_block_coords(self, x, y, chunk_info):
        block = find_grid_box(x, y)

        for y in range(self.chunk_size_y):
            for x in range(self.chunk_size_x):
                x_coord = x * int(TILE_SIZE * SCALING) + chunk_info['left']
                y_coord = y * int(TILE_SIZE * SCALING) + chunk_info['bottom']

                chunk_block = find_grid_box(x_coord, y_coord)

                if block[0] == chunk_block[0] and block[1] == chunk_block[1]:
                    print('find_chunk_block_coords:', x_coord, y_coord)
                    print('find_chunk_block_coords:', x, y)
                    print('find_chunk_block_coords:', self.chunks[chunk_info['index']][y][x])
                    return x, y

    def generate_chunk(self, side):
        print('[ spawn chunk ]')
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


class TreeGenerator:

    def __init__(self, ctx):
        self.ctx = ctx
        self.tree_pos_x = list()
        self.tree_distance = None

    def setup(self):
        self._generate_random_distance()
        self.one(4, 0)

    def _generate_random_distance(self):
        if self.tree_distance is None:
            self.tree_distance = random.randrange(8, 17, 4)

    def one(self, offset_x_blocks, idx):
        tree_shape = random.choice(TREE_SHAPES)
        scaled_tile = int(TILE_SIZE * SCALING)

        if self.tree_pos_x:
            offset_x = offset_x_blocks * scaled_tile + self.tree_pos_x[idx]
        else:
            offset_x = offset_x_blocks * scaled_tile + scaled_tile // 2

        base_tree_x = (len(tree_shape[0]) // 2 + 1) * scaled_tile + offset_x
        offset_y = scaled_tile + scaled_tile // 2

        chunk = self.ctx.world.map_generator.find_chunk(*find_grid_box(base_tree_x, offset_y))
        chunk_block_x, chunk_block_y = self.ctx.world.map_generator.find_chunk_block_coords(
            base_tree_x,
            offset_y,
            chunk
        )

        while True:
            if self.ctx.world.map_generator.chunks[chunk['index']][chunk_block_y][chunk_block_x] != 0:
                offset_y += scaled_tile
                chunk_block_y += 1
            else:
                break

        self.ctx.world.block_list.extend((
            Block(
                scale=SCALING,
                name=BLOCK_IDS[tree_shape[y][x]],
                filename=BLOCK_PATHS[BLOCK_IDS[tree_shape[y][x]]],
                center_x=x * scaled_tile + offset_x,
                center_y=(len(tree_shape) - y) * scaled_tile + offset_y
            ) for x in range(len(tree_shape[0])) for y in range(len(tree_shape)) if tree_shape[y][x] != 0
        ))

        if idx == -1:
            self.tree_pos_x.append(base_tree_x)
        else:
            self.tree_pos_x.insert(idx, base_tree_x)

    def update(self, side):
        self._generate_random_distance()
        detect_range = 12 * int(TILE_SIZE * SCALING)

        if side == 'left':
            if self.ctx.player.center_x < self.tree_pos_x[0] + detect_range:
                self.one(-self.tree_distance, 0)
                self.tree_distance = None

        elif side == 'right':
            if self.tree_pos_x[-1] - detect_range < self.ctx.player.center_x:
                self.one(self.tree_distance, -1)
                self.tree_distance = None
