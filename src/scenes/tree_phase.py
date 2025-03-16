import pygame

from enviorement.background import Background
from enviorement.camera import Camera
from enviorement.tilemap import Tilemap
from entities.player import Player
from entities.mushroom import Mushroom
from resource_manager import ResourceManager
from scenes.phase import Phase
from sound_manager import SoundManager
from utils.constants import HEIGHT, WIDTH


class TreePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.foreground = Tilemap("tiled/levels/tree.tmx")
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)
        self.background = Background(self.resources, "assets\\images\\backgrounds\\tree_phase_parallax", enable_vertical_scroll=True)
        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}

        self.lights_group = pygame.sprite.Group()


        # Mushrooms
        bouncy_obstacles = []
        mushrooms = self.foreground.load_layer_entities("mushrooms")
        self.mushrooms_group = pygame.sprite.Group()
        for mushroom in mushrooms.values():
            mushroom = Mushroom(mushroom.x, mushroom.y)
            bouncy_obstacles.append(mushroom.platform_rect)
            self.mushrooms_group.add(mushroom)
            self.lights_group.add(mushroom.light)

        # Player
        player_spawn = self.foreground.load_entity("player_spawn")
        self.player = Player(player_spawn.x, player_spawn.y, self.foreground, bouncy_obstacles)


    def update(self):
        dt = self.director.clock.get_time() / 1000

        self.player.update(self.pressed_keys, dt)

        # Mushrooms
        self.mushrooms_group.update()
        for mushroom in self.mushrooms_group:
            if self.player.rect.colliderect(mushroom.platform_rect):
                mushroom.glow = True
                mushroom.bounce = True

        # Player dying logic
        if pygame.sprite.spritecollideany(self.player, self.lights_group):
            self.player.is_dying = True
        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")

        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
        for mushroom in self.mushrooms_group:
            mushroom.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
