import pygame
from scene import Scene
from utils.constants import *
from scenes.pauseMenu import PauseMenu
from scenes.startMenu import StartMenu
from scenes.end_menu import EndMenu
from scenes.cemetery_phase import CemeteryPhase
from scenes.cemeteryBossPhase import CemeteryBossPhase
from scenes.tree_phase import TreePhase
from scenes.lake_phase import LakePhase
from scene_manager import SceneManager
from sound_manager import SoundManager
from scenes.minigamePhase import MinigamePhase

class Director:
    """
    Singleton class that manages the core game loop, scene stack, rendering, 
    and interactions between scenes and systems like sound and scene registration.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.scenes_stack: list[Scene] = []
            cls.leave_current_scene: bool = False
            cls.clock: pygame.time.Clock = pygame.time.Clock()
            cls.screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
            cls.scene_manager: SceneManager = SceneManager(cls._instance)
            cls.setup_scenes(cls)
            cls.sound_manager: SoundManager = SoundManager()
            cls.restart_flag: bool = False
        return cls._instance

    def get_current_scene_name(self) -> str:
        """
        Returns the class name of the currently active scene.
        """
        return self.scenes_stack[-1].__class__.__name__

    def setup_scenes(self):
        """
        Registers all available scenes with the scene manager.
        """
        self.scene_manager.register_scene("StartMenu", StartMenu)
        self.scene_manager.register_scene("PauseMenu", PauseMenu)
        self.scene_manager.register_scene("LakePhase", LakePhase)
        self.scene_manager.register_scene("EndMenu", EndMenu)
        self.scene_manager.register_scene("CemeteryPhase", CemeteryPhase)
        self.scene_manager.register_scene("CemeteryBossPhase", CemeteryBossPhase)
        self.scene_manager.register_scene("TreePhase", TreePhase)
        self.scene_manager.register_scene("LakePhase", LakePhase)
        self.scene_manager.register_scene("MinigamePhase", MinigamePhase)

    def finish_current_scene(self):
        """
        Flags the current scene to be exited and pops it from the stack.
        Also sets a restart flag for the upcoming scene.
        """
        self.leave_current_scene = True
        if self.scenes_stack:
            self.scenes_stack.pop()
            self.restart_flag = True

    def finish_program(self):
        """
        Exits all scenes and clears the stack, effectively ending the game.
        """
        self.leave_current_scene = True
        self.scenes_stack = []

    def change_scene(self, scene: Scene):
        """
        Replaces the current scene with a new one.
        """
        self.finish_current_scene()
        self.scenes_stack.append(scene)

    def stack_scene(self, scene: Scene):
        """
        Pushes a new scene onto the stack while marking the current one to pause.
        Useful for temporary overlays like pause menus.
        """
        self.leave_current_scene = True
        self.scenes_stack.append(scene)

    def loop(self, scene: Scene):
        """
        Main loop for a given scene. Handles timing, event processing, 
        updates, and rendering until the scene is flagged to exit.
        """
        self.leave_current_scene = False
        pygame.event.clear()

        while not self.leave_current_scene:
            self.clock.tick(60)

            if self.restart_flag:
                self.restart_flag = False
                scene.continue_procedure()

            scene.events(pygame.event.get())
            scene.update()
            scene.draw()
            pygame.display.update()

    def run(self):
        """
        Runs the main game loop, executing the top scene on the stack.
        """
        while self.scenes_stack:
            self.loop(self.scenes_stack[-1])
