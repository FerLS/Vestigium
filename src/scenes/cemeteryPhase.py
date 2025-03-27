from time import sleep
import pygame
from enviorement.tilemap import Tilemap
from gui.gui_elements.guiText import InitialInstructionText, RetryInstructionText
from scenes.phase import Phase
from utils.constants import *
from enviorement.background import Background
from resource_manager import ResourceManager
from sound_manager import SoundManager
from entities.player import Player
from enviorement.camera import Camera
from entities.gravedigger import Gravedigger
from entities.firefly import Firefly
from trigger import Trigger, change_scene
from scenes.fadeTransition import FadeTransition, FadeIn, FadeOut
from light2 import ConeLight  # Import ConeLight


class CemeteryPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}
        
        area_rect = pygame.Rect(500, 500, 300, 200)
        self.firefly = Firefly(600, 600, area_rect)
        
        self.lamppost_blink_timer = 0
        self.lamppost_blink_state = 1

        self.fade_out = FadeOut(self.screen, 1, on_complete= lambda: change_scene(self.director, "MinigamePhase"))        

        self.instruction_text = None
        self.instruction_timer = 0
        
        self.load_resources()
        self.setup_groups()
        self.setup_enemies()
        self.setup_player()
        self.setup_triggers()
        self.setup_audio()
        
    def load_resources(self):
        """
        Load all resources needed for the scene.
        """
        self.foreground = Tilemap("tiled/levels/test_level.tmx")
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.background = Background(
            self.resources, "assets\\images\\backgrounds\\parallax_forest"
        )
    
    def setup_groups(self):
        """
        Setup the sprite groups and trigger list for the scene.
        """
        self.lampposts_group = pygame.sprite.Group()
        self.lights_group = pygame.sprite.Group(self.firefly.light)
        self.triggers = []
        
    def setup_enemies(self):
        """
        Setup the entities for the scene.
        """
        self.create_lampposts()
        
    def setup_player(self):
        """
        Create the player entity.
        """
        spawn_coords = self.foreground.load_entity("player_spawn")
        self.player = Player(spawn_coords.x, spawn_coords.y, self.foreground, obstacles = [])
        
    def setup_triggers(self):
        """
        Setup the triggers for the scene.
        """
        self.init_trigger("cemetery_end", lambda: self.fade_out.start())
        if not self.director.restarted:
                self.init_trigger("start_trigger", lambda: self.start_trigger())
        else:
            self.init_trigger("start_trigger", lambda: self.start_trigger())
            self.init_trigger("start_again_trigger", lambda: self.start_again_trigger())
    
    def setup_audio(self):
        """
        Setup the audio for the scene.
        """
        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)
        
    def create_lampposts(self):
        """
        Create lampposts with associated ConeLight objects.
        Assign a unique blink offset to each lamppost.
        """
        lamppost_positions = self.foreground.load_layer_entities("lampposts")
        for index, lamppost in enumerate(lamppost_positions.values()):
            light = ConeLight(
                (lamppost.x, lamppost.y),
                direction=(0, 1),
                angle=40,
                distance=200,
                fixed_position=(lamppost.x, lamppost.y)
            )
            light.blink_offset = index * 2
            self.lampposts_group.add(light)
            self.lights_group.add(light)
            
    def init_trigger(self, entity_name: str, callback: callable):
        """
        Initialize a trigger with a callback function.
        """
        end_coords = self.foreground.load_entity(entity_name)
        self.end_phase_rect = pygame.Rect(end_coords.x, end_coords.y, end_coords.width, end_coords.height)
        self.triggers.append(Trigger(self.end_phase_rect, callback))
    
    def start_trigger(self):
        """
        Action to be triggered when the player starts.
        """
        self.instruction_text = InitialInstructionText(self.screen, (WIDTH // 5, WIDTH // 8))
        self.instruction_timer = 10  # Display for 10 seconds
        
    def start_again_trigger(self):
        """
        Action to be triggered when the player starts after dying.
        """
        self.instruction_text = RetryInstructionText(self.screen, (WIDTH // 5, WIDTH // 8))
        self.instruction_timer = 5 

    def update(self):
        dt = self.director.clock.get_time() / 1000
        # Update entities
        self.player.update(self.pressed_keys, dt)
        self.firefly.update()

        # Update triggers
        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)

        # Lamppost blink
        self.lamppost_blink_timer += dt
        for light in self.lampposts_group:
            adjusted_timer = (self.lamppost_blink_timer - light.blink_offset) % 6
            if 0 <= adjusted_timer < 1:  # Fade in
                light.intensity = adjusted_timer
            elif 1 <= adjusted_timer < 3:  # Stay on
                light.intensity = 1
            elif 3 <= adjusted_timer < 4:  # Fade out
                light.intensity = 1 - (adjusted_timer - 3)
            elif 4 <= adjusted_timer < 6:  # Stay off
                light.intensity = 0

        # Update lights
        for light in self.lampposts_group:
            light.update(dt)
            
        # Collision detection with delay
        in_collision = any(light.intensity > 0 and self.player.check_pixel_perfect_collision(light) for light in self.lights_group)

        if in_collision:
            self.collision_delay_timer += dt  # Start counting
            if self.collision_delay_timer >= 0.25: 
                self.player.is_dying = True
        else:
            self.collision_delay_timer = 0  # Reset timer if no collision
        """
        for light in self.lights_group:
            if light.intensity > 0 and self.player.check_pixel_perfect_collision(light): 
                self.player.is_dying = True
        """
        
        # Restart if dead
        if self.player.dead:
            self.director.restarted = True
            self.director.scene_manager.stack_scene("CemeteryPhase")
        
        self.fade_out.update(dt)
        self.camera.update(self.player.rect)

        if self.instruction_timer > 0:
            self.instruction_timer -= dt
            if self.instruction_timer <= 0:
                self.instruction_text = None

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
        self.firefly.draw(self.screen, offset)
        
        for light in self.lampposts_group:
            light.draw(self.screen, offset)
        
        for trigger in self.triggers:
            trigger.draw(self.screen)

        if self.instruction_text:
            self.instruction_text.draw(self.screen)

        self.fade_out.draw()
