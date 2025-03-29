from types import SimpleNamespace
import pygame
from utils.fade_transition import FadeIn, FadeOut
from scenes.phase import Phase
from entities.npcs.firefly import Firefly
from entities.players.key import Key
from entities.objects.lock import Lock
from entities.objects.lifes import Lifes

class MinigamePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        
        self.load_resources(background_path="assets/images/backgrounds/minigame_background")
        self.setup_camera()
        self.setup_groups()
        self.setup_entities()
        self.setup_player()
        self.setup_enemies()
        self.setup_audio()
        self.setup_fades()
    
    def setup_groups(self):
        """
        Setup all sprite groups
        """
        self.fireflies_group = pygame.sprite.Group()
        self.lights_group = pygame.sprite.Group()
    
    def setup_entities(self):
        """
        Setup all entities
        """
        self.lifes = Lifes()
        self.lock = Lock(0, 100, self.screen.get_width())

    def setup_player(self):
        """
        Setup the player entity
        """
        self.key = Key()
    
    def revive_player(self):
        # Not implemented as this phase has unique gameplay mechanics.
        pass
    
    def setup_spawns(self):
        # Not needed in this phase; spawns are irrelevant here.
        pass

    def move_player_to_spawn(self):
        # Not required; player positioning is handled differently.
        pass

    def increment_spawn_index(self):
        # Not used; spawn indexing is unnecessary in this phase.
        pass

    def init_trigger(self, entity_name, callback, triggered_once=True):
        # Triggers are not part of this phase's mechanics.
        pass

    def setup_triggers(self):
        # No triggers needed for this phase's gameplay.
        pass

    def end_of_phase(self):
        # Not implemented as this phase has unique change scene mechanics
        pass

    def setup_enemies(self):
        """
        Setup all enemies
        """
        self.create_fireflies()

    def create_fireflies(self):
        """
        Setup all firefly enemies
        """
        fireflies = {
            "1": SimpleNamespace(x=100, y=100),
            "2": SimpleNamespace(x=450, y=150),
            "3": SimpleNamespace(x=900, y=200),
            "4": SimpleNamespace(x=550, y=250),
            "5": SimpleNamespace(x=100, y=300),
            "6": SimpleNamespace(x=450, y=350),
            "7": SimpleNamespace(x=900, y=400),
            "8": SimpleNamespace(x=550, y=450),  
        }

        for firefly in fireflies.values():
            firefly = Firefly(firefly.x, firefly.y, None, "wave")
            firefly_extra = Firefly(500, 150, None, "random")
            self.fireflies_group.add(firefly)
            self.fireflies_group.add(firefly_extra)
            self.lights_group.add(firefly.light)
            self.lights_group.add(firefly_extra.light)
            
    def setup_audio(self):
        """
        Setup the audio for the scene.
        """
        self.sound_manager.play_music("minigame_music.mp3", "assets\\music", -1)

    def setup_fades(self):
        """
        Setup all fade effects for the scene.
        """
        self.fades = {}
        fade_in = FadeIn(self.screen)
        fade_in.start()
        self.fades = {
            'fade_in': fade_in,
            'fade_out_win': FadeOut(self.screen, on_complete=lambda: self.director.scene_manager.stack_scene("TreePhase")),
            'fade_out_loose': FadeOut(self.screen, on_complete=lambda: self.director.scene_manager.stack_scene("CemeteryBossPhase")),
        }
    
    def update(self):
        dt = self.director.clock.get_time() / 1000

        if self.manage_life_animation():
            return

        self.key.update(self.lock, self.lifes.ammount)
        self.lock.update(dt, self.key)
        self.fireflies_group.update()
        self.lifes.update()

        self.manage_life_logic()
        
        if pygame.sprite.collide_mask(self.key, self.lock):
            for firefly in self.fireflies_group:
               firefly.stop()
            if self.lock.end:
                self.fades['fade_out_win'].start()

        for fade in self.fades.values():
            fade.update(dt)  

    def manage_life_animation(self):
        """
        Check if the life animation is active and update it.
        """
        if self.lifes.animating:
            self.lifes.update()
            if self.lifes.ammount == 0 and not self.lifes.animating:
                for firefly in self.fireflies_group:
                    firefly.stop()
                self.fades['fade_out_loose'].start()
            elif not self.lifes.animating:
                for firefly in self.fireflies_group:
                    firefly.reset("life_decreased")
            return True
        else:
            return False

    def manage_life_logic(self):
        """
        Check if the player is colliding with the fireflies and decrease life if so.
        """
        if pygame.sprite.spritecollide(self.key, self.lights_group, False, pygame.sprite.collide_mask):
            if self.lifes.ammount > 0:
                self.lifes.decrease()
                self.key.reset()
                for firefly in self.fireflies_group:
                    firefly.reset("life_decreased", delay=True)
            else:
                for firefly in self.fireflies_group:
                    firefly.stop()
                self.lifes.decrease()
        
    def draw(self):        
        self.background.draw(self.screen, (0, 0))

        for firefly in self.fireflies_group:
            firefly.draw(self.screen)

        self.lifes.draw(self.screen)

        self.lock.draw(self.screen)

        self.key.draw(self.screen)

        for fade in self.fades.values():
            fade.draw()
            
    def continue_procedure(self):
        self.sound_manager.play_sound(
            "forest_ambient.wav", "assets\\sounds", category="ambient", loop=True
        )
