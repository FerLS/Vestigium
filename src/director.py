import pygame
from utils.constants import *
from scenes.pauseMenu import PauseMenu
from scenes.startMenu import StartMenu
from scenes.dyingMenu import DyingMenu
from scenes.cemeteryPhase import CemeteryPhase
from scenes.tree_phase import TreePhase
from scenes.lake_phase import LakePhase
from scene_manager import SceneManager
from scenes.minigamePhase import MinigamePhase

class Director(object):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.scenes_stack = []
            cls.leave_current_scene = False
            cls.clock = pygame.time.Clock()
            cls.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            cls.scene_manager = SceneManager(cls._instance)
            cls.setup_scenes(cls)
            cls.restarted = False

        return cls._instance

    def get_current_scene_name(self):
        return self.scenes_stack[-1].__class__.__name__

    def setup_scenes(self):
        self.scene_manager.register_scene("StartMenu", StartMenu)
        self.scene_manager.register_scene("PauseMenu", PauseMenu)
        self.scene_manager.register_scene("DyingMenu", DyingMenu)
        self.scene_manager.register_scene("CemeteryPhase", CemeteryPhase)
        self.scene_manager.register_scene("TreePhase", TreePhase)
        self.scene_manager.register_scene("LakePhase", LakePhase)
        self.scene_manager.register_scene("MinigamePhase", MinigamePhase)
    
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