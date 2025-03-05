import pygame
from enviorement.tilemap import Tilemap
from scenes.phase import Phase 
from utils.constants import WIDTH
from enviorement.background import Background
from resource_manager import ResourceManager
from entities.player import Player
from enviorement.camera import Camera
from entities.gravedigger import Gravedigger


class CemeteryPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.foreground = Tilemap("tiled/levels/test_level.tmx")
        self.resources = ResourceManager()
        self.background = Background(self.resources, "assets\\images\\backgrounds\\parallax_forest")
        self.player = Player(WIDTH//2, 100, self.foreground)
        self.camera = Camera()
        self.pressed_keys = {}
        #gravedigger_spawn = tilemap.entities.get("enemy_spawn")
        #gravedigger = Gravedigger(gravedigger_spawn.x, gravedigger_spawn.y, tilemap)

    def update(self):
        self.player.update(self.pressed_keys, self.screen, self.camera.scroll_x, self.camera.scroll_y)
        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")
        self.camera.update(self.player, self.pressed_keys)
        self.foreground.update(self.camera.scroll_x, self.camera.scroll_y) 
        self.background.update(self.camera.scroll_x)
        #self.gravedigger.update(self.player, self.camera.scroll, self.screen)

    def draw(self):
        self.background.draw(self.screen)
        self.foreground.draw(self.screen)
        self.player.draw(self.screen, self.pressed_keys)
        # self.gravedigger.light.draw(self.screen)
    