import pygame 

from scenes.menu import Menu
from gui.gui_screens.dying_screen import DyingScreen

class DyingMenu(Menu):
    def __init__(self, director):
        Menu.__init__(self, director)
        self.screen_list = []
        self.screen_list.append(DyingScreen(self, "menu_background.jpg")) # Self parameter refers to menu
        

    # Static menu (has no sprites that move)
    def update(self, **args):
        return
    
    def events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
            if event.type == pygame.QUIT:
                self.exit_game()
        self.screen_list[-1].events(event_list)

    def draw(self):
        self.screen_list[-1].draw(self.director.screen)
    
    def restart_level(self):
        self.director.finish_current_scene()
        scene_name = self.director.get_current_scene_name()
        self.director.scene_manager.change_scene(scene_name)

    def go_to_main_menu(self):
        self.director.scene_manager.change_scene("StartMenu")
        # continue flag activated
    