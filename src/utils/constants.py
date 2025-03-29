from enum import Enum

# Environment constants
WIDTH, HEIGHT = 1000, 800 # Screen dimensions
SCALE_FACTOR = 2 # Scaling factor for the game
CAMERA_LIMITS_X = 240, 560 # Camera limits for the x-axis
CAMERA_LIMITS_Y = 100, 700 # Camera limits for the y-axis

# Shadow player constants
MOVE_SPEED = 3 
MAX_FALL_SPEED = 10

# Key player movement constants
ACC = 1.2
FRIC = -0.10

# Gravedigger movement constants
class MovementDirections(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class MovementType(Enum):
    IDLE = 1
    WALK = 2
    JUMP = 3
