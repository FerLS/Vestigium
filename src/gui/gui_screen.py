from tkinter import Menu
import pygame
import os
from abc import ABC, abstractmethod
from managers.resource_manager import ResourceManager
from utils.constants import WIDTH, HEIGHT

class GUIScreen(ABC):
    """
    Base class for GUI screens in the game. Handles background image animations,
    GUI elements, and user interactions. Subclasses should implement specific GUI behavior.
    """

    def __init__(self, menu: Menu, images_path: str):
        """
        Initializes the GUI screen.

        :param menu: The Menu object that owns this screen.
        :param images_path: Path to the folder containing background images.
        """
        self.menu: Menu = menu
        self.images: list[pygame.Surface] = self._init_images(images_path)
        self.image_index: int = 0
        self.image: pygame.Surface = self.images[self.image_index]
        self.frame_counter: int = 0
        self.gui_elements: list[object] = self._init_gui_elements()

    @abstractmethod
    def _init_gui_elements(self) -> list[object]:
        """
        Initializes GUI elements for the screen. Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def _init_images(self, images_path: str) -> list[pygame.Surface]:
        """
        Loads and scales background images from the specified path.

        :param images_path: Path to the folder containing background images.
        :return: A list of scaled pygame.Surface objects.
        """
        images = []
        for file in os.listdir(images_path):
            if file.endswith(".png"):
                image = ResourceManager().load_image(file, images_path)
                scaled_image = pygame.transform.scale(image, (WIDTH, HEIGHT))
                images.append(scaled_image)
        return images

    def update(self) -> None:
        """
        Updates the background animation and checks for hover interactions
        with GUI elements.
        """
        # Update background animation
        self.frame_counter = (self.frame_counter + 1) % 15
        if self.frame_counter == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]

        # Update hover state for GUI elements
        mouse_pos = pygame.mouse.get_pos()
        for element in self.gui_elements:
            element.update_hover(mouse_pos)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the background and GUI elements on the screen.

        :param screen: The pygame.Surface to draw on.
        """
        screen.blit(self.image, (0, 0))
        for element in self.gui_elements:
            element.draw(screen)

    def events(self, event_list: list[pygame.event.Event]) -> None:
        """
        Handles user input events, such as mouse clicks, for GUI elements.

        :param event_list: A list of pygame events to process.
        """
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_button_up(event)

    def _handle_mouse_button_down(self, event: pygame.event.Event) -> None:
        """
        Handles mouse button down events.

        :param event: The pygame event to process.
        """
        self.clicked_element = None
        for element in self.gui_elements:
            if element.position_in_element(event.pos):
                self.clicked_element = element

    def _handle_mouse_button_up(self, event: pygame.event.Event) -> None:
        """
        Handles mouse button up events.

        :param event: The pygame event to process.
        """
        for element in self.gui_elements:
            if element.position_in_element(event.pos):
                if element == self.clicked_element:
                    element.action()