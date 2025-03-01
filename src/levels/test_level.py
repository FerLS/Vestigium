from enviorement.tilemap import Tilemap
from levels.scene import Scene
from utils.constants import SCALE_FACTOR, WIDTH, HEIGHT
from enviorement.background import Background
from resource_manager import ResourceManager
from entities.player import Player
from enviorement.camera import Camera
from entities.gravedigger import Gravedigger


class TestLevel(Scene):
    tilemap = Tilemap("tiled/levels/test_level.tmx")
    resources = ResourceManager()
    foreground = tilemap
    background = Background(resources, "assets\\images\\backgrounds\\parallax_forest")
    player = Player(WIDTH // 2, 100, tilemap)
    camera = Camera()

    gravedigger_spawn = tilemap.entities.get("enemy_spawn")
    gravedigger = Gravedigger(gravedigger_spawn.x, gravedigger_spawn.y, tilemap)

    def __init__(self, screen):
        super().__init__(self.tilemap, screen)
        self.screen = screen

    def update(self, keys_pressed):
        super().update()
        self.player.update(keys_pressed, self.screen, self.camera.scroll)
        self.camera.update(self.player.rect, keys_pressed)
        self.foreground.update(self.camera.scroll)  # Ahora se mueve correctamente
        self.background.update(self.camera.scroll)
        self.gravedigger.update(self.player, self.camera.scroll, self.screen)

    def draw(self):
        super().draw()
        self.background.draw(self.screen)
        self.foreground.draw(self.screen)
        self.gravedigger.light.draw(self.screen)
