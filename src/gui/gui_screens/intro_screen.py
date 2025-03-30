from tkinter import Menu
import pygame
from gui.gui_element import GUIElement
from gui.gui_screen import GUIScreen
from gui.gui_elements.gui_text import IntroOfGameText, IntroText, GoToStartText
from utils.constants import WIDTH, HEIGHT

class IntroScreen(GUIScreen):
    """
    Represents the introduction screen of the game. Displays an initial message, a lore text,
    and a button to start the game.
    """
    def __init__(self, menu: Menu):
        """
        Initializes the intro screen.

        :param menu: The Menu object that owns this screen.
        """
        self.menu: object = menu
        self.image: pygame.Surface = None  # No background image for the intro screen
        self.gui_elements: list[GUIElement] = self._init_gui_elements()
    
    def _init_gui_elements(self) -> list[GUIElement]:
        """
        Initializes the GUI elements for the intro screen.

        :return: A list of GUI elements (e.g., intro message, intro-of-game text, "Go to Start" button).
        """
        gui_elements = []
        gui_elements.append(IntroText(self, (100, 100))) # Intro message
        gui_elements.append(IntroOfGameText(self, (WIDTH/2 - 90, HEIGHT/1.5))) # Intro-of-game text
        gui_elements.append(GoToStartText(self, (WIDTH/2 - 65, HEIGHT/1.2))) # Go to start
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