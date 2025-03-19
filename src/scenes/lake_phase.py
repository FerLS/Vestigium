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
from entities.anglerfish import Anglerfish


class LakePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.foreground = Tilemap("tiled/levels/lake.tmx")
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.background = Background(self.resources, "assets\\images\\backgrounds\\lake_phase_background", enable_vertical_scroll=True)

        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}
        area_rect = pygame.Rect(500, 500, 300, 200)

        player_spawn = self.foreground.load_entity("player_spawn")
        self.player = Player(player_spawn.x, player_spawn.y, self.foreground, [])
        self.player.is_swimming = True

        self.anglerfish = Anglerfish(0, 0, 1, 3, 3000)

        self.lights_group = pygame.sprite.Group()

        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)

    def update(self):
        dt = self.director.clock.get_time() / 1000

        self.player.update(self.pressed_keys, dt)
        self.anglerfish.update(dt, self.player.rect.y)

        if pygame.sprite.spritecollideany(self.player, self.lights_group):
            self.player.is_dying = True

        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")

        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
        self.anglerfish.draw(self.screen, camera_offset=offset)
        

    