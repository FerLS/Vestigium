import pygame
from enviorement.tilemap import Tilemap
from scene import Scene
from utils.constants import SCALE_FACTOR, WIDTH, HEIGHT
from director import Director
from enviorement.background import Background
from resource_manager import ResourceManager
from entities.player import Player
from enviorement.camera import Camera
from entities.gravedigger import Gravedigger


class CemeteryPhase(Scene):
    def __init__(self, director: Director, screen):
        super().__init__(director, screen)
        self.screen = screen
        self.foreground = Tilemap("tiled/levels/test_level.tmx")
        self.resources = ResourceManager()
        self.background = Background(self.resources, "assets\\images\\backgrounds\\parallax_forest")
        self.player = Player(WIDTH//2, 100, self.foreground)
        self.camera = Camera()
        self.pressed_keys = {}
        self.screen = screen
        #gravedigger_spawn = tilemap.entities.get("enemy_spawn")
        #gravedigger = Gravedigger(gravedigger_spawn.x, gravedigger_spawn.y, tilemap)

    def update(self):
        self.player.update(self.pressed_keys, self.screen, self.camera.scroll_x, self.camera.scroll_y)
        self.camera.update(self.player, self.pressed_keys)
        self.foreground.update(self.camera.scroll_x, self.camera.scroll_y) 
        self.background.update(self.camera.scroll_x)
        #self.gravedigger.update(self.player, self.camera.scroll, self.screen)

    def draw(self):
        self.background.draw(self.screen)
        self.foreground.draw(self.screen)
        self.player.draw(self.screen, self.pressed_keys)
        # self.gravedigger.light.draw(self.screen)

    def events(self, events: list):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.finish_program()
        self.pressed_keys = pygame.key.get_pressed()


   