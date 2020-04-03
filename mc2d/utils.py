from mc2d.config import SCALING, TILE_SIZE


def find_grid_box(x, y):
    left_x = x - (x % int(TILE_SIZE * SCALING))
    bottom_y = y - (y % int(TILE_SIZE * SCALING))

    center_x = left_x + (TILE_SIZE * SCALING) // 2
    center_y = bottom_y + (TILE_SIZE * SCALING) // 2

    return center_x, center_y
