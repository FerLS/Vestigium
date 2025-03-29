import pygame 

from environment.camera import Camera
from scenes.scene import Scene
from environment.background import Background
from environment.tilemap import Tilemap 
from managers.resource_manager import ResourceManager
from utils.fade_transition import FadeIn, FadeOut
from managers.sound_manager import SoundManager
from utils.trigger import Trigger
from utils.constants import HEIGHT, WIDTH


NOT_IMPLEMENTED_MSG = "Subclasses must implement this method"

class Phase(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)

    def load_resources(self, tilemap_path: str=None, background_path: str=None, enable_vertical_scroll: bool=False, speed_increment: float=0.2):
        """
        Load all resources needed for the scene

        param tilemap_path: Path to the tilemap file
        param background_path: Path to the background image file
        param enable_vertical_scroll: Flag to enable vertical scrolling
        param speed_increment: Speed increment for scrolling

        """

        if tilemap_path:
            self.foreground = Tilemap(tilemap_path)

        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.background = Background(
            self.resources, 
            background_path,
            enable_vertical_scroll=enable_vertical_scroll,
            speed_increment=speed_increment
        )

    def setup_camera(self):
        """
        Setup the camera for the scene.

        """
        self.camera = Camera(WIDTH, HEIGHT)  

    def setup_groups(self):
        """
        Setup all groups for the scene.
        """
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    def setup_enemies(self):
        """
        Setup all enemies for the scene.

        """
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
    
    def setup_spawns(self):
        """
        Setup the spawn points for the scene.
        """
        self.spawns_rects = [pygame.Rect(v.x, v.y, v.width, v.height) for v in self.foreground.load_layer_entities("checkpoints").values()]
        for spawn_rect in self.spawns_rects:
            self.triggers.append(Trigger(spawn_rect, lambda: self.increment_spawn_index()))
        self.spawn_index = -1
        self.current_spawn = self.spawns_rects[self.spawn_index].center

    def increment_spawn_index(self):
        """
        Increment the spawn index.
        """
        self.spawn_index += 1
        self.current_spawn = self.spawns_rects[self.spawn_index].center 
    
    def setup_player(self):
        """
        Setup the player for the scene.

        """
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
    
    def revive_player(self):
        """
        Revive the player entity.

        """
        self.player.dead = False

    def move_player_to_spawn(self):
        """
        Move the camera to the current spawn point.
        """
        self.player.rect.center = self.current_spawn
        self.camera.update(self.player.rect)
        self.fades['revive_fade_in'].start()
    
    def init_trigger(self, entity_name: str, callback: callable, triggered_once: bool=True):
        """
        Initialize a trigger with a callback function.
        """
        entity = self.foreground.load_entity(entity_name)
        trigger_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        self.triggers.append(Trigger(trigger_rect, callback, triggered_once=triggered_once))

    def setup_triggers(self):
        """
        Setup the triggers for the scene using init_trigger generic function.
        """
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
    
    def setup_fades(self, scene_name: str):
        """
        Setup all fade effects for the scene.
        """
        fade_in = FadeIn(self.screen)
        fade_in.start()
        self.fades = {
            'fade_in': fade_in,
            'fade_out': FadeOut(self.screen, on_complete=lambda: self.end_of_phase(scene_name)),
            'revive_fade_in': FadeIn(self.screen, duration=2, on_complete=lambda: self.revive_player()),
            'death_fade_out': FadeOut(self.screen, duration=2, on_complete=lambda: self.move_player_to_spawn())
        }

    def end_of_phase(self, scene_name: str):
        """
        Actions to be executed once the final fade out is finished
        """
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
    
    def setup_audio(self, music_name: str=None, sound_name: str=None):
        """
        Setup the background music and ambient sound effects for the scene.
        """
        if music_name:
            self.sound_manager.play_music(music_name, "assets\\music", -1)
        if sound_name:
            self.sound_manager.play_sound(sound_name, "assets\\sounds", category='ambient', loop=True)

    def update(self, *args):
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
    
    def events(self, events: list):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.finish_program()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.director.scene_manager.stack_scene("PauseMenu")
                    

        self.pressed_keys = pygame.key.get_pressed()
    
    def draw(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)

    def continue_procedure(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)