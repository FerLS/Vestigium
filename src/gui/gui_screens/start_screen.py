from tkinter import Menu
import pygame
from gui.gui_element import GUIElement
from gui.gui_screen import GUIScreen
from gui.gui_elements.gui_text import NewGameText, OptionsText, ExitText
from utils.constants import WIDTH, HEIGHT

class StartScreen(GUIScreen):
    """
    Represents the start screen of the game. Inherits from GUIScreen and initializes
    GUI elements such as "New Game", "Options", and "Exit" buttons.
    """

    def __init__(self, menu: Menu, image_path: str):
        """
        Initializes the start screen.

        :param menu: The Menu object that owns this screen.
        :param image_path: Path to the folder containing background images.
        """
        super().__init__(menu, image_path)

    def _init_gui_elements(self) -> list[GUIElement]:
        """
        Initializes the GUI elements for the start screen.

        :return: A list of GUI elements (e.g., buttons for "New Game", "Options", "Exit").
        """
        gui_elements = []
        gui_elements.append(NewGameText(self, (WIDTH // 2 - 75, 400)))  # "New Game" button
        gui_elements.append(OptionsText(self, (WIDTH // 2 - 71, 440)))  # "Options" button
        gui_elements.append(ExitText(self, (WIDTH // 2 - 55, 480)))     # "Exit" button
        return gui_elements

    def events(self, event_list: list[pygame.event.Event]) -> None:
        """
        Handles user input events for the start screen.

        :param event_list: A list of pygame events to process.
        """
        for event in event_list:
            for element in self.gui_elements:
                element.handle_event(event)