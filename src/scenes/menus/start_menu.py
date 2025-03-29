from scenes.menu import Menu
from gui.gui_screens.start_screen import StartScreen
from gui.gui_screens.options_screen import OptionsScreen

class StartMenu(Menu):
    def __init__(self, director):
        """
        StartMenu class is responsible for displaying the start menu of the game.
        It manages the start screen and options screen.
        """
        Menu.__init__(self, director)
        self.sound_manager.play_music("start_menu.mp3", "assets\\music", -1)
        self.screen_list.append(
            StartScreen(self, "assets\\images\\backgrounds\\main_menu_background")
        )

    def exit_game(self):
        """
        Exit the game by finishing the program.
        """
        self.director.finish_program()

    def play_game(self):
        """
        Start the game by changing the scene to the Introduction scene."""
        self.director.scene_manager.stack_scene(
        "IntroMenu",
        )

    def show_options_screen(self):
        """
        Show the options screen by appending it to the screen list.
        """
        self.screen_list.append(
            OptionsScreen(self, "assets\\images\\backgrounds\\options_menu_background")
        )

    def return_previous_scene(self):
        """
        Remove the last screen from the screen list.
        """
        self.screen_list.pop()
        