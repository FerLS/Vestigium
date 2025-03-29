import pygame
from abc import ABC, abstractmethod
from managers.sound_manager import SoundManager

class GUIElement(ABC):
    """
    Base class for GUI elements in the game. Handles hover and click interactions,
    sound effects, and positioning. Subclasses must implement the `draw` and `action` methods.
    """

    def __init__(self, screen: pygame.Surface, rect: pygame.Rect):
        """
        Initializes the GUI element.

        :param screen: The pygame.Surface where the element will be drawn.
        :param rect: The pygame.Rect defining the element's position and size.
        """
        self.screen: pygame.Surface = screen
        self.rect: pygame.Rect = rect
        self.clicked: bool = False
        self.hovered: bool = False
        self.sound_manager: SoundManager = SoundManager()
        self.hover_sound_flag: bool = True

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        """
        Updates the hover state of the element based on the mouse position.

        :param mouse_pos: The (x, y) position of the mouse.
        """
        self.hovered = self.position_in_element(mouse_pos)
        if self.hovered:
            if self.hover_sound_flag:
                self.hover_sound_flag = False
                self.sound_manager.play_sound("hover.wav", "assets\\sounds")
        else:
            self.hover_sound_flag = True

    def set_position(self, position: tuple[int, int]) -> None:
        """
        Sets the position of the element on the screen.

        :param position: The (x, y) position to move the element to.
        """
        posx, posy = position
        self.rect.x = posx
        self.rect.y = posy

    def position_in_element(self, position: tuple[int, int]) -> bool:
        """
        Checks if a given position is inside the element's boundaries.

        :param position: The (x, y) position to check.
        :return: True if the position is inside the element, False otherwise.
        """
        posx, posy = position
        return self.rect.left <= posx <= self.rect.right and self.rect.top <= posy <= self.rect.bottom

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles mouse events for the element, such as clicks.

        :param event: The pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.clicked = False
            if self.position_in_element(event.pos):
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.position_in_element(event.pos) and self.clicked:
                self.sound_manager.play_sound("click.wav", "assets\\sounds")
                self.action()

    @abstractmethod
    def draw(self) -> None:
        """
        Draws the element on the screen. Must be implemented by subclasses.
        """
        raise NotImplementedError('Draw method must be implemented in subclass')

    @abstractmethod
    def action(self) -> None:
        """
        Defines the action to perform when the element is clicked. Must be implemented by subclasses.
        """
        raise NotImplementedError('Action method must be implemented in subclass')


