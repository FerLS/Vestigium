from time import sleep
import pygame
from enviorement.tilemap import Tilemap
from scenes.phase import Phase 
from utils.constants import WIDTH, HEIGHT
from enviorement.background import Background
from resource_manager import ResourceManager
from sound_manager import SoundManager
from entities.player import Player
from enviorement.camera import Camera
from entities.gravedigger import Gravedigger
from entities.firefly import Firefly
from entities.ant import Ant
from entities.mushroom import Mushroom


class CemeteryPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.foreground = Tilemap("tiled/levels/test_level.tmx")
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.background = Background(self.resources, "assets\\images\\backgrounds\\parallax_forest")

        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}
        area_rect = pygame.Rect(500, 500, 300, 200)
        #gravedigger_spawn = tilemap.entities.get("enemy_spawn")
        #gravedigger = Gravedigger(gravedigger_spawn.x, gravedigger_spawn.y, tilemap)

        

        self.firefly = Firefly(600, 600, area_rect)
        self.ant = Ant(500, 500, area_rect)
        self.mushroom = Mushroom(100, 800)
        self.lights_group = pygame.sprite.Group(self.firefly.light, self.ant.light, self.mushroom.light)
        self.mushrooms_group = pygame.sprite.Group(self.mushroom)

        obstacles = [mushroom.platform_rect for mushroom in self.mushrooms_group]
        self.player = Player(0, WIDTH//2, self.foreground, obstacles)

        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)

    def update(self):
        dt = self.director.clock.get_time() / 1000

        self.player.update(self.pressed_keys, dt)
        self.firefly.update()
        self.ant.update()
        self.mushroom.update()
        
        for mushroom in self.mushrooms_group:
            if self.player.rect.colliderect(mushroom.platform_rect):
                mushroom.glow = True
                mushroom.bounce = True

        if pygame.sprite.spritecollideany(self.player, self.lights_group):
            self.player.is_dying = True

        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")

        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
        self.mushroom.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
        self.firefly.draw(self.screen, offset)
        self.ant.draw(self.screen, offset)
        

    