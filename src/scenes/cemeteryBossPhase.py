import pygame
from enviorement.background import Background
from enviorement.camera import Camera
from enviorement.tilemap import Tilemap
from entities.player import Player
from entities.lantern import Lantern
from entities.keyItem import KeyItem
from entities.gravedigger import Gravedigger
from gui.gui_elements.guiText import BossTutorialText, DoorText, KeyText
from light2 import CircularLight, ConeLight
from scenes.phase import Phase
from scenes.fadeTransition import FadeIn, FadeOut
from trigger import Trigger
from resource_manager import ResourceManager
from sound_manager import SoundManager
from utils.constants import WIDTH, HEIGHT


class CemeteryBossPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.pressed_keys = {}

        self.load_resources()
        self.setup_camera()
        self.setup_spawns()
        self.setup_player()
        self.setup_lantern()
        self.setup_key_item()
        self.setup_gravedigger()
        self.setup_triggers()
        self.setup_audio()
        self.setup_fades()

    def load_resources(self):
        """
        Load all resources needed for the scene.
        """
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.foreground = Tilemap("tiled/levels/cementery_boss.tmx")
        self.background = Background(
            self.resources, "assets\\images\\backgrounds\\parallax_forest"
        )

    def setup_camera(self):
        """
        Setup the camera for the scene.
        """
        self.camera = Camera(WIDTH, HEIGHT)

    def setup_spawns(self):
        """
        Setup the spawn points for the scene.
        """
        self.spawns_rects = [pygame.Rect(v.x, v.y, v.width, v.height) for v in self.foreground.load_layer_entities("checkpoints").values()]
        self.spawn_index = -1
        self.current_spawn = self.spawns_rects[0].center if self.spawns_rects else (0, 0)

    def setup_player(self):
        """
        Create the player entity.
        """
        player_spawn = self.spawns_rects[0].center if self.spawns_rects else (0, 0)
        self.player = Player(player_spawn[0], player_spawn[1], self.foreground, obstacles=[])
        self.foreground.insert_sprite(self.player, 2)

    def revive_player(self):
        self.player.dead = False

    def move_player_to_spawn(self):
        self.player.rect.center = self.current_spawn
        self.camera.update(self.player.rect)
        self.fades['revive_fade_in'].start()

    def setup_lantern(self):
        """
        Create the lantern entity and define its path.
        """
        path_points = {
            int(obj.name): (obj.x, obj.y)
            for obj in self.foreground.tmx_data.objects if obj.type == "Point"
        }
        path_points = [path_points[i] for i in sorted(path_points.keys())]
        self.lantern = Lantern(position=path_points[0], path=path_points, speed=5)
        self.foreground.insert_sprite(self.lantern, -1)

    def setup_key_item(self):
        """
        Create the key item entity.
        """
        key_spawn = self.foreground.load_entity("key_spawn")
        self.key = KeyItem(key_spawn.x, key_spawn.y)
        self.foreground.insert_sprite(self.key, 2)

    def setup_gravedigger(self):
        """
        Create the Gravedigger entity.
        """
        spawn = self.foreground.load_entity("gravedigger_spawn")
        self.gravedigger = Gravedigger(spawn.x, spawn.y, self.foreground)
        self.foreground.insert_sprite(self.gravedigger, 2)

    def setup_triggers(self):
        """
        Setup all triggers in the scene.
        """
        self.triggers = []
        self.init_trigger("tutorial_trigger", lambda: self.boss_tutorial())
        self.init_trigger("end_of_phase", lambda: self.end_of_phase(), triggered_once=False)
        self.init_trigger("key_trigger", lambda: self.show_key_obtained_text())

    def init_trigger(self, entity_name: str, callback: callable, triggered_once: bool = True):
        """
        Initialize a trigger with a callback function.
        """
        entity = self.foreground.load_entity(entity_name)
        trigger_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        self.triggers.append(Trigger(trigger_rect, callback, triggered_once=triggered_once))

    def setup_audio(self):
        """
        Setup all audio for the scene.
        """
        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)

    def setup_fades(self):
        """
        Setup all fade effects for the scene.
        """
        self.fades = {}

        fade_in = FadeIn(self.screen)
        fade_in.start()
        self.fades['fade_in'] = fade_in

        fade_out = FadeOut(self.screen, on_complete=lambda: self.director.scene_manager.change_scene("Minigame"))
        self.fades['fade_out'] = fade_out

        revive_fade_in = FadeIn(self.screen, duration=2, on_complete=lambda: self.revive_player())
        self.fades['revive_fade_in'] = revive_fade_in

        death_fade_out = FadeOut(self.screen, duration=2, on_complete=lambda: self.move_player_to_spawn())
        self.fades['death_fade_out'] = death_fade_out

    def update(self):
        dt = self.director.clock.get_time() / 1000

        self.player.update(self.pressed_keys, dt)
        self.lantern.update(self.player, self.foreground, self.camera.get_offset())

        if self.player.is_dying:
            self.fades['death_fade_out'].start()

        self.gravedigger.update(self.player)
        self.key.update(self.player)

        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)

        for fade in self.fades.values():
            fade.update(dt)

        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)

        for trigger in self.triggers:
            trigger.draw(self.screen)

        for fade in self.fades.values():
            fade.draw()

        self.key.draw(self.screen, offset)

    def boss_tutorial(self):
        text = BossTutorialText(self.screen, (100, 100))
        return text
    
    def show_key_obtained_text(self):
        text = KeyText(self.screen, (100, 100))
        return text

    def continue_procedure(self):
        self.sound_manager.play_sound("forest_ambient.wav", "assets\\sounds", category='ambient', loop=True)

    def end_of_phase(self):
        if self.key.picked:
            self.fades['fade_out'].start()
            return None

        else:
            text = DoorText(self.screen, (100, 100))
            return text

