import pygame
from gui.gui_elements.gui_text import CheckpointText, SwimInstructionText
from utils.light import ConeLight
from scenes.phase import Phase
from utils.constants import SCALE_FACTOR, WIDTH, HEIGHT
from entities.players.player import Player
from entities.npcs.anglerfish import Anglerfish
from entities.npcs.jellyfish import Jellyfish
from environment.camera import Camera

class LakePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen: pygame.Surface = director.screen
        self.pressed_keys: dict = {}

        self.load_resources(
            tilemap_path="tiled/levels/lake.tmx",
            background_path="assets/images/backgrounds/lake_phase_background",
            enable_vertical_scroll=True,
            speed_increment=0.4
            )
        self.setup_groups()
        self.setup_enemies()
        self.setup_camera()
        self.setup_spawns()
        self.setup_player()
        self.setup_triggers()
        self.setup_fades(scene_name="EndMenu")
        self.setup_audio(
            music_name="lake_music.mp3",
            sound_name="bubbles.wav"
            )
        
    def setup_camera(self):
        """
        Redefine superclass setup_camera method to set up the camera for the scene,
          following the fish instead of the player.
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
        self.init_trigger("change_light_angle_trigger_1", lambda: self.change_anglerfish_light(angle=100, distance=400), triggered_once=False)
        self.init_trigger("change_light_angle_trigger_2", lambda: self.change_anglerfish_light(angle=40, distance=300), triggered_once=False)
        self.init_trigger("change_camera_to_player_view_trigger", lambda: self.change_camera_focus(self.player.rect), triggered_once=False)
        self.init_trigger("appear_second_anglerfish_trigger", lambda: self.appear_second_anglerfish(), triggered_once=False)
        self.init_trigger("end_phase_trigger", lambda: self.fades['fade_out'].start())

    def init_trigger(self, entity_name: str, callback: callable, triggered_once: bool=True):
        """
        Initialize a trigger with a callback function.
        """
        entity = self.foreground.load_entity(entity_name)
        trigger_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        self.triggers.append(Trigger(trigger_rect, callback, triggered_once=triggered_once))

    def setup_audio(self):
        """
        Setup the audio for the scene.
        """
        self.sound_manager.play_music("lake_music.mp3", "assets\\music", -1)
        self.sound_manager.play_sound("bubbles.wav", "assets\\sounds", category='ambient', loop=True)

    def setup_spawns(self):
        """
        Setup the spawn points for the scene.
        """
        self.spawns_rects = [pygame.Rect(v.x, v.y, v.width, v.height)
                             for v in self.foreground.load_layer_entities("checkpoints").values()]
        for spawn_rect in self.spawns_rects:
            self.triggers.append(Trigger(spawn_rect, lambda: self.increment_spawn_index()))
        for i, spawn_rect in enumerate(self.spawns_rects):
            if i in [1, 2]:
                self.triggers.append(Trigger(spawn_rect, lambda: self.show_respawn_text()))
        self.spawn_index = -1
        self.current_spawn = self.spawns_rects[self.spawn_index].center

    def setup_player(self):
        """
        Create the player entity.
        """
        player_spawn = self.spawns_rects[0].center
        self.player = Player(
            player_spawn[0], player_spawn[1],
            self.foreground,
            obstacles=[],
            camera=self.camera,
        )
        self.player.is_swimming = True

    def move_player_to_spawn(self):
        """
        Move the camera and player to the current spawn point.
        """
        self.player.rect.center = self.current_spawn
        self.anglerfish.rect.center = (self.current_spawn[0] - 1000, self.current_spawn[1])
        self.camera.update_x_margin(40, WIDTH * 0.75)
        self.camera.margin_y = HEIGHT // 5
        self.camera_focus = self.anglerfish.rect
        
        if self.anglerfish_2 is not None:
            self.anglerfishes_group.remove(self.anglerfish_2)
            self.anglerfish_2 = None
        self.fades['revive_fade_in'].start()

    def setup_fades(self):
        """
        Setup all fade effects for the scene.
        """
        fade_in = FadeIn(self.screen)
        fade_in.start()
        self.fades = {
            'fade_in': fade_in,
            'fade_out': FadeOut(self.screen, on_complete=lambda: self.end_of_phase("EndMenu")),
            'revive_fade_in': FadeIn(self.screen, duration=2, on_complete=lambda: self.revive_player()),
            'death_fade_out': FadeOut(self.screen, duration=2, on_complete=lambda: self.move_player_to_spawn())
        }

    def increment_spawn_index(self):
        """
        Increment the spawn index.
        """
        self.spawn_index += 1
        self.current_spawn = self.spawns_rects[self.spawn_index].center
        
    def show_respawn_text(self):
        text = CheckpointText(self.screen, (WIDTH // 4, WIDTH // 1.4))
        return text

    def update(self):
        dt = self.director.clock.get_time() / 1000

        # Update entities
        self.player.update(self.pressed_keys, dt)
        self.anglerfishes_group.update(dt, player_position=self.player.rect.center)
        for jellyfish in self.jellyfishes_group:
            jellyfish.update(dt)

        # Player dying logic
        for anglerfish in self.anglerfishes_group:
            if self.player.check_pixel_perfect_collision(anglerfish.light) and not self.player.is_dying and not self.player.dead:
                self.player.dying()
                self.fades['death_fade_out'].start()

        if pygame.sprite.spritecollideany(self.player, self.lights_group) and not self.player.is_dying and not self.player.dead:
            self.player.dying()
            self.fades['death_fade_out'].start()

        # Triggers
        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)

        # Fades
        for fade in self.fades.values():
            fade.update(dt)

        # Camera
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

        # Draw fades
        for fade in self.fades.values():
            fade.draw()

    def create_fish(self):
        """
        Create the anglerfish entity.
        """
        spawn = self.foreground.load_entity("fish_spawn_1")
        self.anglerfish = Anglerfish(spawn.x, spawn.y, 1, 3, 3000, light_obstacles=self.foreground.get_collision_rects())
        self.anglerfishes_group.add(self.anglerfish)
        self.anglerfish_2_spawn = self.foreground.load_entity("fish_spawn_2")
        self.anglerfish_2 = None

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
        if self.anglerfish_2 is None:
            self.anglerfish_2 = Anglerfish(self.anglerfish_2_spawn.x, self.anglerfish_2_spawn.y, 1, 3, 3000, light_obstacles=self.foreground.get_collision_rects())
            self.anglerfishes_group.add(self.anglerfish_2)

    def end_of_phase(self, scene: str):
        """
        Action that ends the phase.
        """
        self.director.scene_manager.change_scene(scene)

    def continue_procedure(self):
        self.sound_manager.play_sound("bubbles.wav", "assets\\sounds", category='ambient', loop=True)
