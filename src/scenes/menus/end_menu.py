from gui.gui_screens.end_screen import EndScreen
from scenes.menu import Menu

class EndMenu(Menu):
    """
    EndMenu class is responsible for displaying the end screen of the game.
    """
    def __init__(self, director):
        Menu.__init__(self, director)
        self.sound_manager.stop_all_sounds()
        self.screen_list.append(EndScreen(self))

    def go_to_main_menu(self):
        """
        Change the current scene to the start menu.
        """
        self.director.scene_manager.change_scene("StartMenu")
