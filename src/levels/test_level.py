from enviorement.tilemap import Tilemap
from levels.scene import Scene
from utils.constants import SCALE_FACTOR
from pytmx.util_pygame import load_pygame


tilemap = Tilemap("tiled/test_level.tmx")


class TestLevel(Scene):
    def __init__(self, screen):
        super().__init__(tilemap, screen)
