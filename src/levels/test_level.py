from enviorement.tilemap import Tilemap
from levels.scene import Scene
from utils.constants import SCALE_FACTOR, TILE_SIZE, WIDTH, HEIGHT
from enviorement.background import Background
from resource_manager import ResourceManager
from entities.player import Player
from enviorement.camera import Camera

tilemap = Tilemap("tiled/levels/test_level.tmx")


class TestLevel(Scene):
    def __init__(self, screen):
        super().__init__(tilemap, screen)

    resources = ResourceManager()
    foreground = tilemap
    background = Background(resources, "assets\\images\\backgrounds\\parallax_forest")
    player = Player(WIDTH // 2, 100, tilemap)
    camera = Camera(240, 560)

    def update(self, keys_pressed):
        self.player.update(keys_pressed)
        self.camera.update(self.player.rect)
        self.background.update(self.camera.scroll)
        self.foreground.update(self.camera.scroll)
        self.player.fix_scroll(self.camera.scroll)

    def draw(self):
        self.background.draw(self.screen)
        self.foreground.draw(self.screen)
        self.player.draw(self.screen)
