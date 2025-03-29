import pygame

from gui.gui_screens.end_screen import EndScreen
from scenes.menu import Menu
from managers.sound_manager import SoundManager 

class EndMenu(Menu):
    def __init__(self, director):
        Menu.__init__(self, director)
        self.sound_manager = SoundManager()
        self.sound_manager.stop_all_sounds()
        self.screen_list = [EndScreen(self)]

    def update(self, **args):
        self.screen_list[-1].update(**args)
    
    def go_to_main_menu(self):
        self.director.scene_manager.change_scene("StartMenu")