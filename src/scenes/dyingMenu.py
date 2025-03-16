import pygame 

from scenes.menu import Menu
from gui.gui_screens.dying_screen import DyingScreen

class DyingMenu(Menu):
    def __init__(self, director):
        Menu.__init__(self, director)
        self.screen_list = []
        self.screen_list.append(DyingScreen(self, "assets\\images\\backgrounds\\pause_menu_background"))
        
    def update(self, **args):
        self.screen_list[-1].update(**args)
    
    def restart_level(self):
        self.director.finish_current_scene()
        scene_name = self.director.get_current_scene_name()
        self.director.scene_manager.change_scene(scene_name)

    def go_to_main_menu(self):
        self.director.scene_manager.change_scene("StartMenu")
        # continue flag activated
    