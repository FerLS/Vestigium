import pygame 

from scenes.menu import Menu
from gui.gui_screens.pause_screen import PauseScreen
from gui.gui_screens.options_screen import OptionsScreen
from sound_manager import SoundManager

class PauseMenu(Menu):
    def __init__(self, director):
        Menu.__init__(self, director)
        self.sound_manager = SoundManager()
        self.sound_manager.pause_music()
        self.sound_manager.stop_all_sounds()
        self.screen_list = []
        self.screen_list.append(PauseScreen(self, "assets\\images\\backgrounds\\pause_menu_background")) # Self parameter refers to menu

    def update(self, **args):
        self.screen_list[-1].update(**args)

    def continue_game(self):
        self.sound_manager.resume_music()
        self.director.finish_current_scene()

    def show_options_screen(self):
        self.screen_list.append(OptionsScreen(self, "assets\\images\\backgrounds\\options_menu_background"))

    def go_to_main_menu(self):
        self.director.scene_manager.change_scene("StartMenu")
        # continue flag activated
    
    def restart_level(self):
        self.director.finish_current_scene()
        scene_name = self.director.get_current_scene_name()
        self.director.scene_manager.change_scene(scene_name)
    
    def return_previous_scene(self):
        self.screen_list.pop()
