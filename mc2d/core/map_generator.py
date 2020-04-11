import random


class MapGenerator:

    def __init__(self):
        self.chunks = list()

        self.DIRT_ID = 1
        self.GRASS_ID = 2

    def generate_chunk(self, size_x, size_y, side):
        chunk = [[0 for _ in range(size_x)]for i in range(size_y)]

        # Set the bottom floor
        for y in range(1, 5):
            for x in range(size_x):
                chunk[-y][x] = 1

        layer_size = size_x
        for y in range(size_y - 1):
            if layer_size == 0:
                break

            layer_size = random.randrange(0, layer_size)
            layer_left_pos = random.randint(0, size_x - layer_size)

            for x in range(layer_size):

                # Check if a block is underneath
                if chunk[y - 1][x + layer_left_pos] == self.DIRT_ID:

                    # Check to see if the block is not on the edges
                    if layer_left_pos + x < size_x - 1 and layer_left_pos + x != 0:

                        # Check if there is a block diagonally down left and right
                        if (
                            chunk[y - 1][x + layer_left_pos - 1] == self.DIRT_ID and
                            chunk[y - 1][x + layer_left_pos + 1] == self.DIRT_ID
                        ):
                            chunk[y][x + layer_left_pos] = self.DIRT_ID

        chunk[:-4] = list(reversed(chunk[:-4]))

        grass_count = 0
        run = True
        for y in range(size_y):

            if not run:
                break

            for x in range(size_x):

                if grass_count == size_x:
                    run = False
                    break

                if chunk[y][x] != 0:

                    if y == 0:
                        chunk[y][x] = self.GRASS_ID
                        grass_count += 1

                    # Check to make sure there is not grass or dirt above
                    elif chunk[y - 1][x] not in (self.DIRT_ID, self.GRASS_ID):
                        chunk[y][x] = self.GRASS_ID
                        grass_count += 1

        if side == 'left':
            self.chunks.insert(0, chunk)
        elif side == 'right':
            self.chunks.append(chunk)

        return chunk


if __name__ == '__main__':
    map_gen = MapGenerator()
    chunk = map_gen.generate_chunk(8, 8, 'right')
    print(chunk)
