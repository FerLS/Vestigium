import pygame

from enviorement.background import Background
from enviorement.camera import Camera
from enviorement.tilemap import Tilemap
from entities.player import Player
from entities.mushroom import Mushroom
from entities.ant import Ant
from entities.firefly import Firefly
from light2 import ConeLight, CircularLight
from trigger import Trigger
from resource_manager import ResourceManager
from scenes.phase import Phase
from sound_manager import SoundManager
from utils.constants import HEIGHT, WIDTH, SCALE_FACTOR


class TreePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.foreground = Tilemap("tiled/levels/tree.tmx")
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)
        self.background = Background(
            self.resources,
            "assets\\images\\backgrounds\\tree_phase_parallax",
            enable_vertical_scroll=True,
        )
        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}

        self.lights_group = pygame.sprite.Group()

        # Lights
        left_lights = self.foreground.load_layer_entities("left_lights")
        for left_light in left_lights.values():
            left_ambient_light = ConeLight((left_light.x, left_light.y), 10, 20, 500)
            self.lights_group.add(left_ambient_light)

        self.lights_group.add(
            ConeLight((575 * SCALE_FACTOR, 6842 * SCALE_FACTOR), (0, 1), 20, 10)
        )
        self.lights_group.add(
            CircularLight((575 * SCALE_FACTOR, 6842 * SCALE_FACTOR), 40)
        )

        # Mushrooms
        self.bouncy_obstacles = []
        mushrooms = self.foreground.load_layer_entities("mushrooms")
        self.mushrooms_group = pygame.sprite.Group()
        for mushroom in mushrooms.values():
            mushroom = Mushroom(mushroom.x, mushroom.y)
            self.bouncy_obstacles.append(mushroom.platform_rect)
            self.mushrooms_group.add(mushroom)
            self.lights_group.add(mushroom.light)

        # Ants
        ants = self.foreground.load_layer_entities("ants")
        self.ants_group = pygame.sprite.Group()
        for ant in ants.values():
            ant = Ant(ant.x, ant.y)
            self.ants_group.add(ant)
            self.lights_group.add(ant.light)

        # Fireflies
        fireflies = self.foreground.load_layer_entities("fireflies")
        self.fireflies_group = pygame.sprite.Group()
        movement_bounds = pygame.Rect(
            657 * SCALE_FACTOR,
            6984 * SCALE_FACTOR,
            281 * SCALE_FACTOR,
            2293 * SCALE_FACTOR,
        )
        for firefly in fireflies.values():
            firefly = Firefly(firefly.x, firefly.y, movement_bounds)
            self.fireflies_group.add(firefly)
            self.lights_group.add(firefly.light)

        # Player
        player_spawn = self.foreground.load_entity("player_spawn")
        self.player = Player(
            player_spawn.x, player_spawn.y, self.foreground, self.bouncy_obstacles
        )

        # Triggers
        self.triggers = []

        glide_trigger_rect = pygame.Rect(
            577 * SCALE_FACTOR,
            6921 * SCALE_FACTOR,
            60 * SCALE_FACTOR,
            52 * SCALE_FACTOR,
        )
        glide_trigger = Trigger(
            glide_trigger_rect, lambda: glide(self.screen, self.player)
        )

        camera_margin_trigger_rect = pygame.Rect(
            651 * SCALE_FACTOR,
            6787 * SCALE_FACTOR,
            293 * SCALE_FACTOR,
            219 * SCALE_FACTOR,
        )
        camera_margin_trigger = Trigger(
            camera_margin_trigger_rect,
            lambda: change_camera_y_margin(
                self.camera, self.camera.screen_height // 2.2
            ),
        )

        self.triggers += [glide_trigger, camera_margin_trigger]

    def update(self):
        dt = self.director.clock.get_time() / 1000

        self.player.update(self.pressed_keys, dt)

        # Lights
        self.lights_group.update(
            obstacles=self.foreground.get_collision_rects() + self.bouncy_obstacles
        )

        # Mushrooms
        self.mushrooms_group.update()
        for mushroom in self.mushrooms_group:
            if self.player.rect.colliderect(mushroom.platform_rect):
                mushroom.glow = True
                mushroom.bounce = True

        # Ants
        self.ants_group.update()

        # Fireflies
        self.fireflies_group.update()

        # Player dying logic
        # Player dying logic
        for light in self.lights_group:
            if self.player.rect.colliderect(light.rect):
                print("paso1")
                if light.mask and self.player.mask.overlap(
                    light.mask,
                    (
                        self.player.rect.x - light.rect.x,
                        self.player.rect.y - light.rect.y,
                    ),
                ):
                    print("paso2")
                    self.player.is_dying = True

        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")

        self.camera.update(self.player.rect)

        # Triggers
        for trigger in self.triggers:
            trigger.check(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
        for light in self.lights_group:
            light.draw(self.screen, offset)
        for mushroom in self.mushrooms_group:
            mushroom.draw(self.screen, offset)
        for ant in self.ants_group:
            ant.draw(self.screen, offset)
        for firefly in self.fireflies_group:
            firefly.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
        for trigger in self.triggers:
            trigger.draw(self.screen)
