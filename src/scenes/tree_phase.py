import pygame

from enviorement.background import Background
from enviorement.camera import Camera
from enviorement.tilemap import Tilemap
from entities.player import Player
from entities.mushroom import Mushroom
from entities.ant import Ant
from entities.firefly import Firefly
from gui.gui_elements.guiText import GlideInstructionText
from light2 import ConeLight
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
        self.background = Background(self.resources, "assets\\images\\backgrounds\\tree_phase_parallax", enable_vertical_scroll=True)
        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}

        self.lights_group = pygame.sprite.Group()
        self.pixel_perfect_lights_group = pygame.sprite.Group()

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
        movement_bounds = pygame.Rect(657 * SCALE_FACTOR, 6984 * SCALE_FACTOR, 281 * SCALE_FACTOR, 2293 * SCALE_FACTOR)
        for firefly in fireflies.values():
            firefly = Firefly(firefly.x, firefly.y, movement_bounds)
            self.fireflies_group.add(firefly)
            self.lights_group.add(firefly.light)

        # Player
        player_spawn = self.foreground.load_entity("player_spawn")
        self.player = Player(player_spawn.x, player_spawn.y, self.foreground, self.bouncy_obstacles)

        # Lights
        left_lights = self.foreground.load_layer_entities("left_lights")
        right_lights = self.foreground.load_layer_entities("right_lights")
        for left_light in left_lights.values():
            left_ambient_light = ConeLight((left_light.x, left_light.y), pygame.Vector2(1, 1), 30, 500, segments=10, ray_step=4)
            self.pixel_perfect_lights_group.add(left_ambient_light)

        for right_light in right_lights.values():
            right_ambient_light = ConeLight((right_light.x, right_light.y), pygame.Vector2(-1, 0.6), 30, 500, segments = 10, ray_step=4)
            self.pixel_perfect_lights_group.add(right_ambient_light)

        # Triggers
        self.triggers = []

        r1 = self.foreground.load_entity("glide_trigger")
        glide_trigger_rect = pygame.Rect(r1.x, r1.y, r1.width, r1.height) 
        glide_trigger = Trigger(glide_trigger_rect, lambda: self.glide())
        self.triggers.append(glide_trigger)

        r2 = self.foreground.load_entity("camera_y_margin_trigger")
        camera_margin_trigger_rect = pygame.Rect(r2.x, r2.y, r2.width, r2.height)
        camera_margin_trigger = Trigger(camera_margin_trigger_rect, lambda: self.change_camera_y_margin(self.camera.screen_height // 2.2))
        self.triggers.append(camera_margin_trigger)

        r3 = self.foreground.load_entity("end_of_phase")
        end_of_phase_trigger_rect = pygame.Rect(r3.x, r3.y, r3.width, r3.height)
        end_of_phase_trigger = Trigger(end_of_phase_trigger_rect, lambda: self.end_of_phase())
        self.triggers.append(end_of_phase_trigger)

    def update(self):
        dt = self.director.clock.get_time() / 1000

        self.player.update(self.pressed_keys, dt)

        # Mushrooms
        self.mushrooms_group.update()
        for mushroom in self.mushrooms_group:
            if self.player.rect.colliderect(mushroom.platform_rect):
                mushroom.glow = True
                mushroom.bounce = True

        # Ants
        self.ants_group.update(dt)

        # Fireflies
        self.fireflies_group.update()

        # Lights
        ant_rects = [ant.rect for ant in self.ants_group]
        self.collidable_obstacles = self.foreground.get_collision_rects() + self.bouncy_obstacles + ant_rects
        self.pixel_perfect_lights_group.update(obstacles=self.collidable_obstacles, camera_rect=self.camera.get_view_rect())

        # Player dying logic
        for light in self.pixel_perfect_lights_group:
            if self.player.check_pixel_perfect_collision(light):
                self.player.is_dying = True
        if pygame.sprite.spritecollideany(self.player, self.lights_group):
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

        for light in self.pixel_perfect_lights_group: 
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

    def glide(self):
        text = GlideInstructionText(self.screen, (100, 100))
        self.can_glide = True
        return text

    def change_camera_y_margin(self, new_margin):
        self.camera.margin_y = new_margin
        return None
    
    def end_of_phase(self):
        pass