import random


class MapGenerator:

    def __init__(self):
        self.map = None

        self.DIRT_ID = 1
        self.GRASS_ID = 2

    def generate_chunk(self, size_x, size_y):
        self.map = [[0 for _ in range(size_x)]for i in range(size_y)]

        # Set the bottom floor
        for y in range(1, 5):
            for x in range(size_x):
                self.map[-y][x] = 1

        layer_size = size_x
        for y in range(size_y - 1):
            if layer_size == 0:
                break

            layer_size = random.randrange(0, layer_size)
            layer_left_pos = random.randint(0, size_x - layer_size)

            for x in range(layer_size):

                # Check if a block is underneath
                if self.map[y - 1][x + layer_left_pos] == self.DIRT_ID:

                    # Check to see if the block is not on the edges
                    if layer_left_pos + x < size_x - 1 and layer_left_pos + x != 0:

                        # Check if there is a block diagonally down left and right
                        if (
                            self.map[y - 1][x + layer_left_pos - 1] == self.DIRT_ID and
                            self.map[y - 1][x + layer_left_pos + 1] == self.DIRT_ID
                        ):
                            self.map[y][x + layer_left_pos] = self.DIRT_ID

        self.map[:-4] = list(reversed(self.map[:-4]))

        grass_count = 0
        for y in range(size_y):
            for x in range(size_x):
                
                if grass_count == size_x:
                    return

                if self.map[y][x] != 0:

                    if y == 0:
                        self.map[y][x] = self.GRASS_ID
                        grass_count += 1

                    elif self.map[y - 1][x] not in (self.DIRT_ID, self.GRASS_ID):
                        self.map[y][x] = self.GRASS_ID
                        grass_count += 1


if __name__ == '__main__':
    map_gen = MapGenerator()
    map_gen.generate_chunk(8, 8)
    print(map_gen.map)
