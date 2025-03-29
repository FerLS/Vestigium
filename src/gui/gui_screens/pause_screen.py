from tkinter import Menu
import pygame
from gui.gui_element import GUIElement
from utils.constants import WIDTH
from gui.gui_screen import GUIScreen
from gui.gui_elements.gui_text import ContinueText, OptionsText, GoToMainMenuText, RestartLevel

class PauseScreen(GUIScreen):
    """
    Represents the pause screen of the game. Inherits from GUIScreen and initializes
    GUI elements such as "Continue", "Restart Level", "Options", and "Go to Main Menu" buttons.
    """

    def __init__(self, menu: Menu, image_path: str):
        """
        Initializes the pause screen.

        :param menu: The Menu object that owns this screen.
        :param image_path: Path to the folder containing background images.
        """
        super().__init__(menu, image_path)

    def _init_gui_elements(self) -> list[GUIElement]:
        """
        Initializes the GUI elements for the pause screen.

        :return: A list of GUI elements (e.g., buttons for "Continue", "Restart Level", etc.).
        """
        gui_elements = []
        gui_elements.append(ContinueText(self, (WIDTH // 2 - 75, 360)))  # "Continue" button
        gui_elements.append(RestartLevel(self, (WIDTH // 2 - 67, 400)))  # "Restart Level" button
        gui_elements.append(OptionsText(self, (WIDTH // 2 - 67, 440)))   # "Options" button
        gui_elements.append(GoToMainMenuText(self, (WIDTH // 2 - 83, 480)))  # "Go to Main Menu" button
        return gui_elements

    def events(self, event_list: list[pygame.event.Event]) -> None:
        """
        Handles user input events for the pause screen.

        :param event_list: A list of pygame events to process.
        """
        for event in event_list:
            for element in self.gui_elements:
                element.handle_event(event)