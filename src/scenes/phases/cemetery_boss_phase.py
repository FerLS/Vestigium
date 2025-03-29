import pygame
from entities.players.player import Player
from entities.objects.lantern import Lantern
from entities.objects.key_item import KeyItem
from entities.npcs.gravedigger import Gravedigger
from gui.gui_elements.gui_text import BossStairsText, BossTutorialText, DoorText, KeyText
from scenes.phase import Phase
from utils.constants import SCALE_FACTOR
from utils.fade_transition import FadeTransition
from utils.trigger import Trigger


class CemeteryBossPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen: pygame.Surface = director.screen
        self.pressed_keys: dict = {}

        self.load_resources(tilemap_path="tiled/levels/cemetery_boss.tmx",
                            background_path="assets/images/backgrounds/cemetery_phase_background")
        self.setup_camera()
        self.setup_groups()
        self.setup_spawns(respawn_text_spawns=[1])
        self.setup_player()
        self.setup_enemies()
        self.setup_key_item()
        self.setup_triggers()
        self.setup_fades(scene_name="MinigamePhase")
        self.setup_audio(music_name="mystic_forest.mp3")
    
    def setup_groups(self):
        self.triggers: list[Trigger] = []
        self.fades: dict[FadeTransition] = {}

    def setup_player(self):
        """
        Create the player entity.
        """
        player_spawn = self.spawns_rects[0].center if self.spawns_rects else (0, 0)
        self.player = Player(
            player_spawn[0], player_spawn[1], self.foreground, obstacles=[]
        )
        # Decrease the jump power to make it more difficult in parkour
        self.player.jump_power_coyote = -4 * SCALE_FACTOR
        self.foreground.insert_sprite(self.player, 2)

    def setup_enemies(self):
        """
        Create the enemies in the scene.
        """
        self.setup_gravedigger()
        self.setup_lantern()

    def setup_lantern(self):
        """
        Create the lantern entity and define its path.
        """
        path_points = {
            int(obj.name): (obj.x, obj.y)
            for obj in self.foreground.tmx_data.objects
            if obj.type == "Point"
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
        self.init_trigger("tutorial_trigger", lambda: self.boss_tutorial())
        self.init_trigger("stairs_trigger", lambda: self.stairs_trigger())
        self.init_trigger(
            "end_of_phase", lambda: self.manage_door(), triggered_once=False
        )
        self.init_trigger("key_trigger", lambda: self.show_key_obtained_text())

    def update(self):
        dt = self.director.clock.get_time() / 1000

        # Update entities
        self.player.update(self.pressed_keys, dt)
        self.lantern.update(self.player, self.foreground, self.camera.get_offset())

        # Player dying logic
        if self.player.is_dying:
            self.fades["death_fade_out"].start()

        self.gravedigger.update(self.player)
        self.key.update(self.player)

        # Update triggers
        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)

        # Update fades
        for fade in self.fades.values():
            fade.update(dt)

        # Update camera
        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()
        
        # Draw the background and foreground layers
        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)

        # Draw triggers
        for trigger in self.triggers:
            trigger.draw(self.screen)

        # Draw fades
        for fade in self.fades.values():
            fade.draw()

        self.key.draw(self.screen, offset)

    def boss_tutorial(self):
        """
        Show the tutorial text for the boss phase.
        """
        text = BossTutorialText(self.screen, (100, 100))
        return text
    
    def stairs_trigger(self):
        """
        Show the tutorial for clinbing stairs.
        """
        text = BossStairsText(self.screen, (100, 100))
        return text

    def show_key_obtained_text(self):
        """
        Show the text when the key is obtained.
        """
        self.sound_manager.play_sound("key-clang.wav", "assets\\sounds")
        text = KeyText(self.screen, (100, 100))
        return text

    def continue_procedure(self):
        """
        Continue the procedure after the fade out.
        """
        self.sound_manager.play_sound(
            "forest_ambient.wav", "assets\\sounds", category="ambient", loop=True)

    def end_of_phase(self, scene_name: str):
        """
        End the phase and transition to the next scene.
        """
        self.director.scene_manager.stack_scene(scene_name)

    def manage_door(self):
        """
        Manage the door trigger and let the player pass through it when the key is picked. 
        Otherwise, show the text.
        """
        if self.key.picked:
            self.fades["fade_out"].start()
            self.player.jump_power_coyote = -6 * SCALE_FACTOR
            return None

        else:
            text = DoorText(self.screen, (100, 100))
            return text
