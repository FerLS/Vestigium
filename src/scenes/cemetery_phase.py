import pygame
from enviorement.tilemap import Tilemap
from gui.gui_elements.guiText import InitialInstructionText, RetryInstructionText
from scenes.phase import Phase
from utils.constants import WIDTH, HEIGHT 
from enviorement.background import Background
from resource_manager import ResourceManager
from sound_manager import SoundManager
from entities.player import Player
from enviorement.camera import Camera
from entities.firefly import Firefly
from trigger import Trigger
from scenes.fadeTransition import FadeIn, FadeOut
from light2 import ConeLight 


class CemeteryPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}
                        
        self.load_resources()
        self.setup_instructions()
        self.setup_groups()
        self.setup_enemies()
        self.setup_spawns()
        self.setup_player()
        self.setup_triggers()
        self.setup_audio()
        self.setup_fades()
        
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

    def setup_instructions(self):
        """
        Setup the instruction text for the scene.
        """
        self.instruction_text = InitialInstructionText(self.screen, (50, 100))
    
    def setup_groups(self):
        """
        Setup the sprite groups and trigger list for the scene.
        """
        self.lampposts_group = pygame.sprite.Group()
        self.lights_group = pygame.sprite.Group()
        self.fireflies_group = pygame.sprite.Group()
        self.triggers = []
        
    def setup_enemies(self):
        """
        Setup the entities for the scene.
        """
        # Lampposts
        self.create_lampposts()
        
        # Vertical fireflies
        fireflies = self.foreground.load_layer_entities("fireflies_v")
        for firefly in fireflies.values():
            firefly = Firefly(firefly.x, firefly.y, movement_type="vertical")
            self.fireflies_group.add(firefly)
            self.lights_group.add(firefly.light)
        
        # Horizontal fireflies
        fireflies = self.foreground.load_layer_entities("fireflies_h")
        for firefly in fireflies.values():
            firefly = Firefly(firefly.x, firefly.y,movement_type="horizontal")
            self.fireflies_group.add(firefly)
            self.lights_group.add(firefly.light)

    def setup_spawns(self):
        """
        Setup the spawn points for the scene.
        """
        self.spawns_rects = [pygame.Rect(v.x, v.y, v.width, v.height) for v in self.foreground.load_layer_entities("checkpoints").values()]
        for spawn_rect in self.spawns_rects:
            self.triggers.append(Trigger(spawn_rect, lambda: self.increment_spawn_index()))
        self.spawn_index = -1
        self.current_spawn = self.spawns_rects[self.spawn_index].center
        
    def setup_player(self):
        """
        Create the player entity.
        """
        player_spawn = self.spawns_rects[0].center
        self.player = Player(player_spawn[0], player_spawn[1], 
                             self.foreground, 
                             obstacles=[])
        
    def revive_player(self):
        """
        Show instructions and revive the player after dying.
        """
        self.instruction_text = RetryInstructionText(self.screen, (50, 100))
        self.player.dead = False

    def move_player_to_spawn(self):
        """
        Move the camera to the current spawn point.
        """
        self.player.rect.center = self.current_spawn
        self.camera.update(self.player.rect)
        self.fades['revive_fade_in'].start()
        
    def setup_triggers(self):
        """
        Setup the triggers for the scene.
        """
        self.init_trigger("death", lambda: self.fades['death_fade_out'].start(), triggered_once=False)
        self.init_trigger("end_of_phase", lambda: self.fades['fade_out'].start())

    def setup_fades(self):
        """
        Setup all fade effects for the scene.
        """
        fade_in = FadeIn(self.screen)
        fade_in.start()
        self.fades = {
            'fade_in': fade_in,
            'fade_out': FadeOut(self.screen, on_complete=lambda: self.end_of_phase("TreePhase")),
            'revive_fade_in': FadeIn(self.screen, duration=2, on_complete=lambda: self.revive_player()),
            'death_fade_out': FadeOut(self.screen, duration=2, on_complete=lambda: self.move_player_to_spawn())
        }
        
    def increment_spawn_index(self):
        """
        Increment the spawn index.
        """
        self.instruction_text.visible = True
        self.spawn_index += 1
        self.current_spawn = self.spawns_rects[self.spawn_index].center 
    
    def setup_audio(self):
        """
        Setup the audio for the scene.
        """
        self.sound_manager.play_music("cemetery_music.mp3", "assets\\music", -1)
        self.sound_manager.play_sound("cemetery_background_sound.ogg", "assets\\sounds", category='ambient', loop=True)
        
    def create_lampposts(self):
        """
        Create lampposts with associated ConeLight objects.
        Assign a unique blink offset to each lamppost.
        """
        self.lamppost_blink_timer = 0
        self.lamppost_blink_state = 1
        lamppost_positions = self.foreground.load_layer_entities("lampposts")
        for index, lamppost in enumerate(lamppost_positions.values()):
            light = ConeLight(
                (lamppost.x, lamppost.y),
                direction=(0, 1),
                angle=35,
                distance=260,
            )
            light.blink_offset = index * 2
            self.lampposts_group.add(light)
            self.lights_group.add(light)
            
    def init_trigger(self, entity_name: str, callback: callable, triggered_once: bool = True):
        """
        Initialize a trigger with a callback function.
        """
        end_coords = self.foreground.load_entity(entity_name)
        self.end_phase_rect = pygame.Rect(end_coords.x, end_coords.y, end_coords.width, end_coords.height)
        self.triggers.append(Trigger(self.end_phase_rect, callback, triggered_once))  

    def update(self):
        dt = self.director.clock.get_time() / 1000
        
        # Update entities
        self.player.update(self.pressed_keys, dt)
            
        self.fireflies_group.update()
        
        self.lights_group.update()

        # Lamppost blink
        self.lamppost_blink_timer += dt
        for light in self.lampposts_group:
            adjusted_timer = (self.lamppost_blink_timer - light.blink_offset) % 6
            if 0 <= adjusted_timer < 1:  
                light.intensity = adjusted_timer
            elif 1 <= adjusted_timer < 3:  
                light.intensity = 1
            elif 3 <= adjusted_timer < 4:
                light.intensity = 1 - (adjusted_timer - 3)
            elif 4 <= adjusted_timer < 6:
                light.intensity = 0
        
        # Check player dying conditions
        for light in self.lights_group:          
            if light.intensity > 0.4 and self.player.check_pixel_perfect_collision(light) and not self.player.is_dying and not self.player.dead: 
                self.player.dying()
                self.fades['death_fade_out'].start()

        # Update triggers
        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)

        # Update fades
        for fade in self.fades.values():
            fade.update(dt)

        self.instruction_text.update(dt)
        
        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
        
        for firefly in self.fireflies_group:
            firefly.draw(self.screen, offset)
        
        for light in self.lampposts_group:
            light.draw(self.screen, offset)
        
        for trigger in self.triggers:
            trigger.draw(self.screen)

        self.instruction_text.draw(self.screen)

        for fade in self.fades.values():
            fade.draw()

    def continue_procedure(self):
        """
        Action that continues the phase.
        """
        self.sound_manager.play_sound("cemetery_background_sound.ogg", "assets\\sounds", category='ambient', loop=True)

    def end_of_phase(self, scene=str):
        """
        Action that ends the phase.
        """
        self.director.scene_manager.change_scene(scene)