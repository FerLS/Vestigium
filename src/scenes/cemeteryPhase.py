import pygame
from enviorement.tilemap import Tilemap
from scenes.phase import Phase 
from utils.constants import WIDTH
from enviorement.background import Background
from resource_manager import ResourceManager
from sound_manager import SoundManager
from entities.player import Player
from enviorement.camera import Camera
from entities.gravedigger import Gravedigger
from entities.firefly import Firefly


class CemeteryPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.foreground = Tilemap("tiled/levels/test_level.tmx")
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.background = Background(self.resources, "assets\\images\\backgrounds\\parallax_forest")
        self.player = Player(0, WIDTH//2, self.foreground)
        self.camera = Camera()
        self.pressed_keys = {}
        area_rect = pygame.Rect(500, 500, 300, 200)
        self.firefly = Firefly(600, 600, area_rect)
        #gravedigger_spawn = tilemap.entities.get("enemy_spawn")
        #gravedigger = Gravedigger(gravedigger_spawn.x, gravedigger_spawn.y, tilemap)

        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)

    def update(self):
        self.firefly.update()
        self.player.update(self.pressed_keys, self.camera.scroll_x, self.camera.scroll_y, self.director.clock.get_time() / 1000)
        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")
        self.camera.update(self.player, self.pressed_keys)
        self.foreground.update(self.camera.scroll_x, self.camera.scroll_y) 
        self.background.update(self.camera.scroll_x)
        #self.gravedigger.update(self.player, self.camera.scroll, self.screen)

    def draw(self):
        self.background.draw(self.screen)
        self.foreground.draw(self.screen)
        self.player.draw(self.screen)
        self.firefly.draw(self.screen)
        # self.gravedigger.light.draw(self.screen)
    