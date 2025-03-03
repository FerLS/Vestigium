from enum import Enum

WIDTH, HEIGHT = 1000, 800
SCALE_FACTOR = 2
MOVE_SPEED = 5
CAMERA_LIMITS_X = 240, 560
CAMERA_LIMITS_Y = 200, 600
MAX_FALL_SPEED = 10


class MovementDirections(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class MovementType(Enum):
    IDLE = 1
    WALK = 2
    JUMP = 3
