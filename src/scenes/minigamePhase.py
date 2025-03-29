from types import SimpleNamespace
import pygame
from pygame.locals import *

from scenes.fadeTransition import FadeIn, FadeOut
from scenes.phase import Phase
from entities.firefly import Firefly
from entities.key import Key
from entities.lock import Lock
from entities.lifes import Lifes
from resource_manager import ResourceManager
from sound_manager import SoundManager

class MinigamePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        
        self.load_resources()
        self.setup_groups()
        self.setup_entities()
        self.create_fireflies()
        self.setup_audio()
        self.setup_fades()
        
    def load_resources(self):
        """
        Load all resources needed for the scene
        """
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.background = pygame.transform.scale(
            self.resources.load_image(
                "minigame_background.png", 
                "assets/images/backgrounds"
            ),
            (self.screen.get_width(), self.screen.get_height())
        )
    
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
        self.key = Key()
        self.lifes = Lifes()
        self.lock = Lock(0, 100, self.screen.get_width())

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
            #"9": SimpleNamespace(x=50, y=500),
            #"10": SimpleNamespace(x=950, y=550),
            
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

        if self.lifes.animating:
            self.lifes.update()
            if self.lifes.ammount == 0 and not self.lifes.animating:
                for firefly in self.fireflies_group:
                    firefly.stop()
                self.fades['fade_out_loose'].start()
            elif not self.lifes.animating:
                for firefly in self.fireflies_group:
                    firefly.reset("life_decreased")
            return

        self.key.update(self.lock, self.lifes.ammount)
        self.lock.update(dt, self.key)
        self.fireflies_group.update()
        self.lifes.update()
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
        
        if pygame.sprite.collide_mask(self.key, self.lock):
            for firefly in self.fireflies_group:
               firefly.stop()
                
            if self.lock.end:
                self.fades['fade_out_win'].start()
        for fade in self.fades.values():
            fade.update(dt)
                
        
    def draw(self):
        self.screen.blit(self.background, (0, 0))
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