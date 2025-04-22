GRID_SIZE = 20
WIDTH, HEIGHT = 600, 400

def get_speed_for_level(level):
    return max(10, 15 - level)  # Gets faster every level


def get_walls_for_level(level):
    # simple wall patterns based on level
    walls = []
    if level >= 2:
        walls += [(x, 100) for x in range(100, 500, 20)]
    if level >= 3:
        walls += [(x, 300) for x in range(100, 500, 20)]
    return walls