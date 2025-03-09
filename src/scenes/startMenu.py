import pygame 

from scenes.menu import Menu
from gui.gui_screens.start_screen import StartScreen
from gui.gui_screens.options_screen import OptionsScreen

class StartMenu(Menu):
    def __init__(self, director):
        Menu.__init__(self, director)
        self.screen_list = []
        self.screen_list.append(StartScreen(self, "assets\\images\\backgrounds\\main_menu_background")) # Self parameter refers to menu
        

    # Static menu (has no sprites that move)
    def update(self, **args):
        self.screen_list[-1].update(**args)
                
    def exit_game(self):
        self.director.finish_program()

    def play_game(self):
        self.director.scene_manager.stack_scene("CemeteryPhase")

    def show_options_screen(self):
        self.screen_list.append(OptionsScreen(self, "menu_background.jpg"))

    def return_previous_scene(self):
        self.screen_list.pop()
