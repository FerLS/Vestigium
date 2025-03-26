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
from scenes.fadeTransition import FadeOut
from trigger import Trigger
from resource_manager import ResourceManager
from scenes.phase import Phase
from sound_manager import SoundManager
from utils.constants import HEIGHT, WIDTH


class TreePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.pressed_keys = {}

        self.load_resources()
        self.setup_groups()
        self.setup_camera()
        self.setup_enemies()
        self.setup_player()
        self.setup_triggers()
        self.setup_audio()
        self.setup_fade()

    def load_resources(self):
        """
        Load all resources needed for the scene.
        """
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.foreground = Tilemap("tiled/levels/tree.tmx")
        self.background = Background(
            self.resources,
            "assets\\images\\backgrounds\\tree_phase_parallax",
            enable_vertical_scroll=True
        )

    def setup_camera(self):
        """
        Setup the camera for the scene.
        """
        self.camera = Camera(WIDTH, HEIGHT)

    def setup_groups(self):
        """
        Setup the sprite groups and trigger list for the scene.
        """
        self.lights_group = pygame.sprite.Group()
        self.pixel_perfect_lights_group = pygame.sprite.Group()
        self.mushrooms_group = pygame.sprite.Group()
        self.ants_group = pygame.sprite.Group()
        self.fireflies_group = pygame.sprite.Group()
        self.bouncy_obstacles = []
        self.triggers = []

    def setup_audio(self):
        """
        Setup the audio for the scene.
        """
        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)

    def setup_fade(self):
        """
        Setup the fade out transition.
        """
        self.fade_out = FadeOut(self.screen, 1, on_complete=lambda: self.end_of_phase("LakePhase"))

    def setup_enemies(self):
        """
        Setup the entities for the scene.
        """
        self.load_mushrooms()
        self.load_ants()
        self.load_fireflies()
        self.load_static_lights()

    def setup_player(self):
        """
        Create the player entity.
        """
        player_spawn = self.foreground.load_entity("player_spawn")
        self.player = Player(player_spawn.x, player_spawn.y, 
                             self.foreground, 
                             obstacles=self.bouncy_obstacles)

    def load_mushrooms(self):
        """
        Place the mushrooms in the scene and add them to the groups.
        """
        mushrooms = self.foreground.load_layer_entities("mushrooms")
        for data in mushrooms.values():
            mushroom = Mushroom(data.x, data.y)
            self.bouncy_obstacles.append(mushroom.platform_rect)
            self.mushrooms_group.add(mushroom)
            self.lights_group.add(mushroom.light)

    def load_ants(self):
        """
        Place the ants in the scene and add them to the groups.
        """
        ants = self.foreground.load_layer_entities("ants")
        for data in ants.values():
            ant = Ant(data.x, data.y)
            self.ants_group.add(ant)
            self.lights_group.add(ant.light)

    def load_fireflies(self):
        """
        Place the fireflies in the scene and add them to the groups.
        """
        fireflies = self.foreground.load_layer_entities("fireflies")
        bounds = self.foreground.load_entity("movement_bounds")
        movement_bounds = pygame.Rect(bounds.x, bounds.y, bounds.width, bounds.height)
        for data in fireflies.values():
            firefly = Firefly(data.x, data.y, movement_bounds)
            self.fireflies_group.add(firefly)
            self.lights_group.add(firefly.light)

    def load_static_lights(self):
        """
        Place the static lights in the scene and add them to the pixel perfect light group to perform collision with mask.
        """
        left_lights = self.foreground.load_layer_entities("left_lights")
        for light in left_lights.values():
            self.pixel_perfect_lights_group.add(
                ConeLight((light.x, light.y), pygame.Vector2(1, 1), 30, 500, segments=10, ray_step=4)
            ) 

        right_lights = self.foreground.load_layer_entities("right_lights")
        for light in right_lights.values():
            self.pixel_perfect_lights_group.add(
                ConeLight((light.x, light.y), pygame.Vector2(-1, 0.6), 30, 500, segments=10, ray_step=4)
            )

    def setup_triggers(self):
        """
        Setup the triggers for the scene.
        """
        self.init_trigger("glide_trigger", lambda: self.glide())
        self.init_trigger("camera_y_margin_trigger", lambda: self.change_camera_y_margin(self.camera.screen_height // 2.2))
        self.init_trigger("end_of_phase", lambda: self.fade_out.start())

    def init_trigger(self, entity_name: str, callback: callable):
        """
        Initialize a trigger with a callback function.
        """
        entity = self.foreground.load_entity(entity_name)
        trigger_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        self.triggers.append(Trigger(trigger_rect, callback))

    def update(self):
        dt = self.director.clock.get_time() / 1000

        # Update player and entities
        self.player.update(self.pressed_keys, dt)

        self.mushrooms_group.update()

        self.ants_group.update(dt)

        self.fireflies_group.update()

        # Check if the player is colliding with the mushrooms
        for mushroom in self.mushrooms_group:
            if self.player.rect.colliderect(mushroom.platform_rect):
                mushroom.glow = True
                mushroom.bounce = True

        # Check pixel perfect collision of lights and obstacles 
        ant_rects = [ant.rect for ant in self.ants_group]
        self.collidable_obstacles = self.foreground.get_collision_rects() + self.bouncy_obstacles + ant_rects
        self.pixel_perfect_lights_group.update(obstacles=self.collidable_obstacles, camera_rect=self.camera.get_view_rect())

        # Check if the player is colliding with the pixel perfect collisions
        if any(self.player.check_pixel_perfect_collision(light) for light in self.pixel_perfect_lights_group):
            self.player.is_dying = True

        # Check if the player is colliding with lights with rects
        if pygame.sprite.spritecollideany(self.player, self.lights_group):
            self.player.is_dying = True

        # Check player dying condition
        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")

        # Update and check triggers
        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)

        # Update camera
        self.camera.update(self.player.rect)

        # Update fade out transition
        self.fade_out.update(dt)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)

        self.foreground.draw(self.screen, offset)

        # Draw pixel perfect lights (lights of enemies are drawn in their respective draw method)
        for light in self.pixel_perfect_lights_group:
            light.draw(self.screen, offset)

        # Draw entities
        for group in [self.mushrooms_group, self.ants_group, self.fireflies_group]:
            for entity in group:
                entity.draw(self.screen, offset)

        self.player.draw(self.screen, camera_offset=offset)

        # Draw triggers text if it exists
        for trigger in self.triggers:
            trigger.draw(self.screen)

        # Draw fade out transition
        self.fade_out.draw()

    # Actions that can be triggered by a Trigger
    def glide(self):
        """
        Enable the player to glide and display the instruction text.
        """
        text = GlideInstructionText(self.screen, (100, 100))
        self.player.can_glide = True
        return text

    def change_camera_y_margin(self, new_margin: int):
        """
        Change the y margin of the camera.
        """
        self.camera.margin_y = new_margin
        return None

    def end_of_phase(self, scene: str):
        """
        Change the scene to the next phase.
        """
        self.director.scene_manager.change_scene(scene)
        return None