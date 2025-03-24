import sys
import time
import pygame
from pygame.locals import *

from scenes.phase import Phase
from utils.constants import Fireflies as Fire, GlobalState, Minigame
from entities.firefly2 import Firefly
from entities.key import Key
from entities.lock import Lock
from entities.lifes import Lifes
from resource_manager import ResourceManager

class MinigamePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        resource_manager = ResourceManager()
        self.background = pygame.transform.scale(
            resource_manager.load_image(
                "minigame_background.png", 
                "assets/images/backgrounds"
            ),
            (director.screen.get_width(), director.screen.get_height())
        )

        self.key = Key()
        self.lock = Lock(0, 100, director.screen.get_width())
        self.fireflies = pygame.sprite.Group()
        self.lifes = Lifes()
        self.lights_group = pygame.sprite.Group()

        self.num_fireflies = 6
        for _ in range(self.num_fireflies // 2):
            firefly = Firefly(Fire.RIGHT)
            firefly.reset()
            self.fireflies.add(firefly)
            self.lights_group.add(firefly.light)
        for _ in range(self.num_fireflies // 2):
            firefly = Firefly(Fire.LEFT)
            firefly.reset()
            self.fireflies.add(firefly)
            self.lights_group.add(firefly.light)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                GlobalState.GAME_STATE = Minigame.GAME_END
                return False
        return True

    def update(self):
        dt = self.director.clock.get_time() / 1000

        if not self.handle_events():
            return

        if self.lifes.animating:
            self.lifes.update()
            if self.lifes.ammount == 0 and not self.lifes.animating:
                self.game_over()
            return

        self.key.update(self.lock)
        self.lock.update(dt, self.key)
        self.fireflies.update(dt)
        self.lifes.update()

        if pygame.sprite.spritecollide(self.key, self.lights_group, False, pygame.sprite.collide_mask):
            if self.lifes.ammount > 0:
                self.lifes.decrease()
                self.key.reset()
                for firefly in self.fireflies:
                    firefly.reset()
            else:
                self.lifes.decrease()
                for firefly in self.fireflies:
                    firefly.stop()

        if pygame.sprite.collide_mask(self.key, self.lock):
            for firefly in self.fireflies:
                firefly.stop()
                
            if self.lock.end:
                self.next_phase()
           
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.lock.draw(self.screen)
        for firefly in self.fireflies:
            firefly.draw(self.screen)
        self.key.draw(self.screen)
        self.lifes.draw(self.screen)

    def game_over(self):
        self.director.scene_manager.stack_scene("DyingMenu")
        
    def next_phase(self):
        self.director.scene_manager.stack_scene("PauseMenu")