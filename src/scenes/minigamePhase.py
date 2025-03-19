import sys
import time
import pygame
from pygame.locals import *

from scenes.phase import Phase
from utils.constants import Fireflies as Fire, GlobalState, Minigame
from entities.firefly2 import Firefly
from entities.key import Key
from entities.lock import Lock


class MinigamePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.background = pygame.transform.scale(
            pygame.image.load("assets/images/backgrounds/minigame_background.png"), 
            (director.screen.get_width(), director.screen.get_height())
        )

        self.key = Key()
        self.lock = Lock(0, 100, director.screen.get_width(), self.game_over)
        self.fireflies = pygame.sprite.Group()

        self.num_fireflies = 6
        for _ in range(self.num_fireflies // 2):
            firefly = Firefly(Fire.RIGHT)
            firefly.reset()
            self.fireflies.add(firefly)
        for _ in range(self.num_fireflies // 2):
            firefly = Firefly(Fire.LEFT)
            firefly.reset()
            self.fireflies.add(firefly)

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

        self.key.update(self.lock)
        self.lock.update(dt, self.key)
        self.fireflies.update(dt)

        if pygame.sprite.spritecollide(self.key, self.fireflies, False, pygame.sprite.collide_mask):
            time.sleep(0.5)
            self.game_over()
            
        if pygame.sprite.collide_mask(self.key, self.lock):
            for firefly in self.fireflies:
                firefly.stop()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.lock.draw(self.screen)
        self.fireflies.draw(self.screen)
        self.key.draw(self.screen)

    def game_over(self):
        GlobalState.GAME_STATE = Minigame.GAME_END
        self.key.reset()
        time.sleep(0.5)