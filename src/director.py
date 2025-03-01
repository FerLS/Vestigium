import pygame
from utils.constants import *

class Director(object):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.scenes_stack = []
            cls.leave_current_scene = False
            cls.clock = pygame.time.Clock()
            cls.screen = pygame.display.set_mode((WIDTH, HEIGHT))


        return cls._instance
    
    def finish_current_scene(self):
        self.leave_current_scene = True
        if self.scenes_stack:
            self.scenes_stack.pop()

    def finish_program(self):
        self.leave_current_scene = True
        self.scenes_stack = []
    
    def change_scene(self, scene):
        self.finish_current_scene()
        self.scenes_stack.append(scene)
    
    def stack_scene(self, scene):
        self.leave_current_scene = True
        self.scenes_stack.append(scene)

    def loop(self, scene):
        self.leave_current_scene = False
        pygame.event.clear()

        while not self.leave_current_scene:
            self.clock.tick(60)
            scene.events(pygame.event.get())
            scene.update()
            scene.draw()
            pygame.display.update()
    
    def run(self):
        while self.scenes_stack:
            self.loop(self.scenes_stack[-1])