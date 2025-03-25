import pygame
from enviorement.tilemap import Tilemap
from gui.gui_elements.guiText import SwimInstructionText
from light2 import ConeLight
from scenes.phase import Phase
from trigger import Trigger
from utils.constants import SCALE_FACTOR, WIDTH, HEIGHT
from enviorement.background import Background
from resource_manager import ResourceManager
from sound_manager import SoundManager
from entities.player import Player
from entities.anglerfish import Anglerfish
from entities.jellyfish import Jellyfish
from enviorement.camera import Camera

class LakePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.pressed_keys = {}

        self.load_resources()
        self.setup_groups()
        self.setup_enemies()
        self.setup_camera()
        self.setup_player()
        self.setup_triggers()
        self.setup_audio()

    def load_resources(self):
        """
        Load all resources needed for the scene.
        """
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.foreground = Tilemap("tiled/levels/lake.tmx")
        self.background = Background(
            self.resources,
            "assets\\images\\backgrounds\\lake_phase_background",
            speed_increment=0.4,
            enable_vertical_scroll=True
        )

    def setup_camera(self):
        """
        Setup the camera for the scene.
        """
        self.camera = Camera(WIDTH, HEIGHT)
        self.camera.update_x_margin(40, WIDTH * 0.75)
        self.camera.margin_y = HEIGHT // 5
        self.camera_focus = self.anglerfish.rect

    def setup_groups(self):
        """
        Setup the sprite groups and trigger list for the scene.
        """
        self.anglerfishes_group = pygame.sprite.Group()
        self.jellyfishes_group = pygame.sprite.Group()
        self.lights_group = pygame.sprite.Group()
        self.triggers = []

    def setup_enemies(self):
        """
        Setup the entities for the scene.
        """
        self.create_fish()
        self.create_jellyfishes()

    def setup_triggers(self):
        """
        Setup the triggers for the scene.
        """
        self.init_trigger("can_swim_trigger", lambda: self.swim())
        self.init_trigger("change_light_angle_trigger_1", lambda: self.change_anglerfish_light(angle=100, distance=400))
        self.init_trigger("change_light_angle_trigger_2", lambda: self.change_anglerfish_light(angle=40, distance=300))
        self.init_trigger("change_camera_to_player_view_trigger", lambda: self.change_camera_focus(self.player.rect))
        self.init_trigger("appear_second_anglerfish_trigger", lambda: self.appear_second_anglerfish())
        self.init_trigger("end_phase_trigger", lambda: self.end_phase())

    def setup_audio(self):
        """
        Setup the audio for the scene.
        """
        self.sound_manager.play_music("lake.wav", "assets\\music", -1)

    def update(self):
        dt = self.director.clock.get_time() / 1000
        self.player.update(self.pressed_keys, dt)
        self.anglerfishes_group.update(dt, player_position=self.player.rect.center)

        # Update jellyfishes
        for jellyfish in self.jellyfishes_group:
            jellyfish.update(dt)

        # Check for collisions pixel perfect with fish light
        for anglerfish in self.anglerfishes_group:
            if self.player.check_pixel_perfect_collision(anglerfish.light):
                self.player.is_dying = True

        # Check for collisions with jellyfishes
        if pygame.sprite.spritecollideany(self.player, self.lights_group):
            self.player.is_dying = True

        # Check for player dying condition
        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")

        # Update and ckeck triggers
        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)
        
        # Update camera
        self.camera.update(self.camera_focus)

    def draw(self):
        offset = self.camera.get_offset()
    
        self.background.draw(self.screen, offset)

        # Draw entities that appear behind the foreground
        for jellyfish in self.jellyfishes_group:
            jellyfish.draw(self.screen, offset)

        self.foreground.draw(self.screen, offset)

        self.player.draw(self.screen, camera_offset=offset)

        # Draw entities that appear in front of the foreground
        for anglerfish in self.anglerfishes_group:
            anglerfish.draw(self.screen, camera_offset=offset)

        # Draw triggers text if it exists
        for trigger in self.triggers:
            trigger.draw(self.screen)

    def setup_player(self):
        """
        Create the player entity.
        """
        player_spawn = self.foreground.load_entity("player_spawn")
        self.player = Player(
            player_spawn.x, player_spawn.y,
            self.foreground, [], self.camera,
            self.anglerfish.light
        )
        self.player.is_swimming = True

    def create_fish(self):
        """
        Create the anglerfish entity.
        """
        spawn = self.foreground.load_entity("fish_spawn_1")
        self.anglerfish = Anglerfish(spawn.x, spawn.y, 1, 3, 3000, light_obstacles=self.foreground.get_collision_rects())
        self.anglerfishes_group.add(self.anglerfish)

    def create_jellyfishes(self):
        """
        Create the jellyfish entities.
        """
        jellyfish_layers = {
            "top_jellyfish": {"axis": "vertical", "direction": -1},
            "bot_jellyfish": {"axis": "vertical", "direction": 1},
            "go_left_jellyfish": {"axis": "horizontal", "direction": -1},
            "go_right_jellyfish": {"axis": "horizontal", "direction": 1},
        }

        for layer_name, config in jellyfish_layers.items():
            entities = self.foreground.load_layer_entities(layer_name)
            for jelly in entities.values():
                jellyfish = Jellyfish(
                    jelly.x, jelly.y,
                    initial_direction=config["direction"],
                    move_axis=config["axis"]
                )
                self.jellyfishes_group.add(jellyfish)
                self.lights_group.add(jellyfish.light)

    def init_trigger(self, entity_name: str, callback: callable):
        """
        Initialize a trigger with a callback function.
        """
        entity = self.foreground.load_entity(entity_name)
        trigger_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        self.triggers.append(Trigger(trigger_rect, callback))

    # Actions that can be triggered by a Trigger
    def swim(self):
        """
        Action to be triggered when the player can swim.
        """
        text = SwimInstructionText(self.screen, (WIDTH // 4, WIDTH // 1.4))
        self.player.is_swimming = True
        return text

    def change_anglerfish_light(self, angle: int, distance: int):
        """
        Change the angle and distance of the anglerfish light.

        param: angle: The angle of the light.
        param: distance: The distance of the light.
        """
        self.anglerfish.light = ConeLight(
            (self.anglerfish.rect.topright[0] - 40, self.anglerfish.rect.topright[1] + 35),
            100 * SCALE_FACTOR,
            segments=10,
            angle=angle,
            distance=distance
        )

    def change_camera_focus(self, camera_focus: pygame.Rect):
        """
        Change the focus of the camera.

        param: camera_focus: The new focus of the camera.
        """
        self.camera_focus = camera_focus
        self.camera.update_x_margin(WIDTH // 4, WIDTH // 4)
        self.camera.margin_y = HEIGHT // 4

    def appear_second_anglerfish(self):
        """
        Action that makes a second fish appear.
        """
        spawn = self.foreground.load_entity("fish_spawn_2")
        self.anglerfish_2 = Anglerfish(spawn.x, spawn.y, 1, 3, 3000, light_obstacles=self.foreground.get_collision_rects())
        self.anglerfishes_group.add(self.anglerfish_2)

    def end_phase(self):
        """
        Action that ends the phase.
        """
        self.sound_manager.stop_music()
        self.director.scene_manager.stack_scene("FinalCutscene")
