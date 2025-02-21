from enum import Enum

WIDTH, HEIGHT = 800, 600
SCALE_FACTOR = 2
TILE_SIZE = 16


class MovementDirections(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class MovementType(Enum):
    IDLE = 1
    WALK = 2
    JUMP = 3
