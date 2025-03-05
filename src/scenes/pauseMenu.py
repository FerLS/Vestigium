import pygame 

from scenes.menu import Menu
from gui.gui_screens.pause_screen import PauseScreen
from gui.gui_screens.options_screen import OptionsScreen

class PauseMenu(Menu):
    def __init__(self, director):
        Menu.__init__(self, director)
        self.screen_list = []
        self.screen_list.append(PauseScreen(self, "menu_background.jpg")) # Self parameter refers to menu
        

    # Static menu (has no sprites that move)
    def update(self, **args):
        return

    def continue_game(self):
        self.director.finish_current_scene()

    def show_options_screen(self):
        self.screen_list.append(OptionsScreen(self, "menu_background.jpg"))

    def go_to_main_menu(self):
        self.director.scene_manager.change_scene("StartMenu")
        # continue flag activated
    
    def restart_level(self):
        self.director.finish_current_scene()
        scene_name = self.director.get_current_scene_name()
        self.director.scene_manager.change_scene(scene_name)
    
    def return_previous_scene(self):
        self.screen_list.pop()

    # def continue_from_nearest_checkpoint()