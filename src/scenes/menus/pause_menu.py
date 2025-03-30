from scenes.menu import Menu
from gui.gui_screens.pause_screen import PauseScreen
from gui.gui_screens.options_screen import OptionsScreen

class PauseMenu(Menu):
    """
    PauseMenu class is responsible for displaying the pause menu of the game. 
    It manages the pause screen and options screen.
    """
    def __init__(self, director):
        Menu.__init__(self, director)
        self.sound_manager.pause_music()
        self.sound_manager.stop_all_sounds()
        self.screen_list.append(PauseScreen(self, "assets\\images\\backgrounds\\pause_menu_background"))

    def continue_game(self):
        """
        Continue the game by resuming the music and finishing the current scene (PauseMenu scene).
        """
        self.sound_manager.resume_music()
        self.director.finish_current_scene()

    def show_options_screen(self):
        """
        Show the options screen by appending it to the screen list.
        """
        self.screen_list.append(OptionsScreen(self, "assets\\images\\backgrounds\\options_menu_background"))

    def go_to_main_menu(self):
        """
        Change the current scene to the start menu and finish the current scene (PauseMenu scene).
        """
        self.director.scene_manager.change_scene("StartMenu")
    
    def restart_level(self):
        """
        Restart the current level by finishing the current scene (PauseMenu scene) and changing the scene to the current one.
        """
        self.director.finish_current_scene()
        scene_name = self.director.get_current_scene_name()
        if scene_name == "MinigamePhase":
            scene_name = "CemeteryBossPhase"
        self.director.scene_manager.change_scene(scene_name)
    
    def return_previous_scene(self):
        """
        Remove the last screen from the screen list.
        """
        self.screen_list.pop()
