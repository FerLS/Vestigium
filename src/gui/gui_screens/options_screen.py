from tkinter import Menu
import pygame
from gui.gui_element import GUIElement
from gui.gui_screen import GUIScreen
from gui.gui_elements.gui_text import MusicVolumeText, SoundEffectsVolumeText, GoBackText
from gui.gui_elements.gui_slider import MusicVolumeSlider, SoundEffectsVolumeSlider
from utils.constants import WIDTH

class OptionsScreen(GUIScreen):
    """
    Represents the options screen of the game. Inherits from GUIScreen and initializes
    GUI elements such as sliders for music and sound effects volume, and a "Go Back" button.
    """

    def __init__(self, menu: Menu, image_path: str):
        """
        Initializes the options screen.

        :param menu: The Menu object that owns this screen.
        :param image_path: Path to the folder containing background images.
        """
        super().__init__(menu, image_path)

    def _init_gui_elements(self) -> list[GUIElement]:
        """
        Initializes the GUI elements for the options screen.

        :return: A list of GUI elements (e.g., sliders for volume control, "Go Back" button).
        """
        gui_elements = []
        gui_elements.append(MusicVolumeText(self, (WIDTH // 2 - 50, 360)))  # Music volume label
        gui_elements.append(MusicVolumeSlider(self, WIDTH // 2 - 75, 390, 125, 10))  # Music volume slider
        gui_elements.append(SoundEffectsVolumeText(self, (WIDTH // 2 - 120, 420)))  # Sound effects volume label
        gui_elements.append(SoundEffectsVolumeSlider(self, WIDTH // 2 - 75, 450, 125, 10))  # Sound effects slider
        gui_elements.append(GoBackText(self, (WIDTH // 2 - 70, 500)))  # "Go Back" button
        return gui_elements

    def events(self, event_list: list[pygame.event.Event]) -> None:
        """
        Handles user input events for the options screen.

        :param event_list: A list of pygame events to process.
        """
        for event in event_list:
            for element in self.gui_elements:
                element.handle_event(event)
