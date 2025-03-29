from enum import Enum

WIDTH, HEIGHT = 1000, 800
SCALE_FACTOR = 2
MOVE_SPEED = 3
CAMERA_LIMITS_X = 240, 560
CAMERA_LIMITS_Y = 100, 700
MAX_FALL_SPEED = 10

ACC = 1.2
FRIC = -0.10

class MovementDirections(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class MovementType(Enum):
    IDLE = 1
    WALK = 2
    JUMP = 3

class Fireflies(Enum):
    RIGHT = 0
    LEFT = 1
