import pygame 

from scene import Scene
from gui.gui_screens.start_screen import StartScreen
from gui.gui_screens.config_screen import ConfigScreen

from scenes.cemeteryPhase import CemeteryPhase

class StartMenu(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        self.screen_list = []
        self.current_screen = 0
        self.screen_list.append(StartScreen(self, "menu_background.jpg")) # Self parameter refers to menu
        self.screen_list.append(ConfigScreen(self, "menu_background.jpg"))

    # Static menu (has no sprites that move)
    def update(self, **args):
        return
    
    def events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
                elif event.type == pygame.QUIT:
                    self.exit_game()
        self.screen_list[self.current_screen].events(event_list)

    def draw(self):
        self.screen_list[self.current_screen].draw(self.director.screen)
                
    def exit_game(self):
        self.director.finish_program()

    def play_game(self):
        phase = CemeteryPhase(self.director)
        self.director.stack_scene(phase)

    def show_start_screen(self):
        self.current_screen = 0

    def show_config_screen(self):
        self.current_screen = 1