import pygame 

from scenes.scene import Scene
from gui.gui_screen import GUIScreen
from managers.sound_manager import SoundManager

class Menu(Scene):
    """
    Base class for all menus in the game. 
    It manages the screens and sound for the menu.
    """
    def __init__(self, director):
        Scene.__init__(self, director)
        self.screen_list: list[GUIScreen] = []
        self.sound_manager: SoundManager = SoundManager()

    def update(self) -> None:
        """
        Update the current screen in the menu.

        :return: None
        """
        self.screen_list[-1].update()
    
    def events(self, events: list) -> None:
        """
        Handle QUIT event for the current screen in the menu and pass other events to it.

        :param events: List of events to handle.
        :return: None
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.director.finish_program()
        self.screen_list[-1].events(events)
    
    def draw(self) -> None:
        """
        Draw the current screen in the menu.
        """
        self.screen_list[-1].draw(self.director.screen)
    
    def continue_procedure(self):
        # This method is intentionally left empty as menus always start from 0
        pass