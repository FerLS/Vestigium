import pygame
from enviorement.tilemap import Tilemap
from scenes.phase import Phase 
from trigger import Trigger, swim, chage_anglerfish_light_1, chage_anglerfish_light_2
from utils.constants import SCALE_FACTOR, WIDTH, HEIGHT
from enviorement.background import Background
from resource_manager import ResourceManager
from sound_manager import SoundManager
from entities.player import Player
from entities.anglerfish import Anglerfish
from entities.jellyfish import Jellyfish
from enviorement.camera import Camera
from entities.anglerfish import Anglerfish


class LakePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.foreground = Tilemap("tiled/levels/lake.tmx")
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.background = Background(self.resources, "assets\\images\\backgrounds\\lake_phase_background", speed_increment=0.4, enable_vertical_scroll=True)

        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}

        self.lights_group = pygame.sprite.Group()

        # Fish 
        anglerfish_spawn = self.foreground.load_entity("fish_spawn")
        self.anglerfish = Anglerfish(anglerfish_spawn.x, anglerfish_spawn.y, 1, 3, 3000, light_obstacles=self.foreground.get_collision_rects())

        # Jellyfish
        top_jellyfishes = self.foreground.load_layer_entities("top_jellyfish")
        bot_jellyfishes = self.foreground.load_layer_entities("bot_jellyfish")
        self.jellyfishes_group = pygame.sprite.Group()

        for jellyfish in top_jellyfishes.values():
            jellyfish = Jellyfish(jellyfish.x, jellyfish.y, initial_direction=-1)
            self.jellyfishes_group.add(jellyfish)
            self.lights_group.add(jellyfish.light)

        for jellyfish in bot_jellyfishes.values():
            jellyfish = Jellyfish(jellyfish.x, jellyfish.y, initial_direction=1)
            self.jellyfishes_group.add(jellyfish)
            self.lights_group.add(jellyfish.light)

        # PLayer
        player_spawn = self.foreground.load_entity("player_spawn")
        self.player = Player(player_spawn.x, player_spawn.y, self.foreground, [], self.camera, self.anglerfish.light)
        self.player.is_swimming = True

        # Triggers
        self.triggers = []

        swim_trigger_rect = pygame.Rect(328 * SCALE_FACTOR, 937 * SCALE_FACTOR, 313 * SCALE_FACTOR, 198 * SCALE_FACTOR) 
        swim_trigger = Trigger(swim_trigger_rect, lambda: swim(self.screen, self.player))

        change_light_angle_trigger_rect_1 = pygame.Rect(2960 * SCALE_FACTOR, 904 * SCALE_FACTOR, 184 * SCALE_FACTOR, 260 * SCALE_FACTOR) 
        change_light_angle_trigger_1 = Trigger(change_light_angle_trigger_rect_1, lambda: chage_anglerfish_light_1(self.anglerfish))

        change_light_angle_trigger_rect_2 = pygame.Rect(6030 * SCALE_FACTOR, 936 * SCALE_FACTOR, 84 * SCALE_FACTOR, 190 * SCALE_FACTOR)
        change_light_angle_trigger_2 = Trigger(change_light_angle_trigger_rect_2, lambda: chage_anglerfish_light_2(self.anglerfish))

        self.triggers += [swim_trigger, change_light_angle_trigger_1, change_light_angle_trigger_2]

        self.sound_manager.play_music("lake.wav", "assets\\music", -1)

    def update(self):
        dt = self.director.clock.get_time() / 1000

        self.player.update(self.pressed_keys, dt)

        self.anglerfish.update(dt, player_position=(self.player.rect.x, self.player.rect.y))

        for jellyfish in self.jellyfishes_group:
            jellyfish.update(dt)

        # Player dying logic
        if self.player.check_pixel_perfect_collision(self.anglerfish.light): # Pixel perfect collision with fish
            self.player.is_dying = True
        if pygame.sprite.spritecollideany(self.player, self.lights_group): # Rect collision with other lights
            self.player.is_dying = True

        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")

        # Triggers
        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)

        # Camera
        self.camera.update(self.anglerfish.rect)
        self.camera.update_x_margin(40, WIDTH * 0.75)
        self.camera.margin_y = HEIGHT // 5

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        for jellyfish in self.jellyfishes_group:
            jellyfish.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
        self.anglerfish.draw(self.screen, camera_offset=offset)

        for trigger in self.triggers:
            trigger.draw(self.screen)
        

    