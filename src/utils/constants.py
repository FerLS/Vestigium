from enum import Enum

WIDTH, HEIGHT = 800, 600
SCALE_FACTOR = 1
MOVE_SPEED = 5
CAMERA_LIMITS = 240, 560


class MovementDirections(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class MovementType(Enum):
    IDLE = 1
    WALK = 2
    JUMP = 3
