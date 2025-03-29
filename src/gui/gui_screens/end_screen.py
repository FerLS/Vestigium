from tkinter import Menu
import pygame
from gui.gui_element import GUIElement
from gui.gui_screen import GUIScreen
from gui.gui_elements.gui_text import EndOfGameText, FinalText, GoToMainMenuText
from utils.constants import WIDTH, HEIGHT

class EndScreen(GUIScreen):
    """
    Represents the end screen of the game. Displays a final message, an end-of-game text,
    and a button to return to the main menu.
    """

    def __init__(self, menu: Menu):
        """
        Initializes the end screen.

        :param menu: The Menu object that owns this screen.
        """
        self.menu: object = menu
        self.image: pygame.Surface = None  # No background image for the end screen
        self.gui_elements: list[GUIElement] = self._init_gui_elements()

    def _init_gui_elements(self) -> list[GUIElement]:
        """
        Initializes the GUI elements for the end screen.

        :return: A list of GUI elements (e.g., final message, end-of-game text, "Go to Main Menu" button).
        """
        gui_elements = []
        gui_elements.append(FinalText(self, (100, 100)))  # Final message
        gui_elements.append(EndOfGameText(self, (WIDTH / 2 - 50, HEIGHT / 1.5)))  # End-of-game text
        gui_elements.append(GoToMainMenuText(self, (WIDTH / 2 - 65, HEIGHT / 1.2)))  # "Go to Main Menu" button
        return gui_elements

    def update(self) -> None:
        """
        Updates the hover state of GUI elements based on the mouse position.
        """
        mouse_pos = pygame.mouse.get_pos()
        for element in self.gui_elements:
            element.update_hover(mouse_pos)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the end screen, including all GUI elements.

        :param screen: The pygame.Surface to draw on.
        """
        screen.fill((0, 0, 0))  # Fill the screen with black
        for element in self.gui_elements:
            element.draw(screen)

    def events(self, event_list: list[pygame.event.Event]) -> None:
        """
        Handles user input events for the end screen.

        :param event_list: A list of pygame events to process.
        """
        for event in event_list:
            for element in self.gui_elements:
                element.handle_event(event)