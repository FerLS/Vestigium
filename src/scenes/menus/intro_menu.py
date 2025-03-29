from gui.gui_screens.intro_screen import IntroScreen
from scenes.menu import Menu

class IntroMenu(Menu):
    """
    IntroMenu class is responsible for displaying the introduction screen of the game.
    """
    def __init__(self, director):
        Menu.__init__(self, director)
        self.sound_manager.play_music("intro_menu.mp3", "assets\\music", -1)
        self.screen_list = [IntroScreen(self)]
    
    def go_to_start(self):
        """
        Change the current scene to the first phase.
        """
        self.director.scene_manager.change_scene("CemeteryPhase")