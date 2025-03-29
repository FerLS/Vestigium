import pygame
from abc import ABC
from gui.gui_element import GUIElement
from managers.sound_manager import SoundManager

class Slider(GUIElement):
    """
    Represents a generic slider GUI element. Allows the user to adjust a value
    by dragging a knob along a horizontal bar.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        min_value: float = 0,
        max_value: float = 1,
        initial_value: float = 0.5,
    ):
        """
        Initializes the slider.

        :param screen: The pygame.Surface where the slider will be drawn.
        :param x: The x-coordinate of the slider's position.
        :param y: The y-coordinate of the slider's position.
        :param width: The width of the slider.
        :param height: The height of the slider.
        :param min_value: The minimum value of the slider.
        :param max_value: The maximum value of the slider.
        :param initial_value: The initial value of the slider.
        """
        super().__init__(screen, pygame.Rect(x, y, width, height))
        self.min_value: float = min_value
        self.max_value: float = max_value
        self.value: float = initial_value
        self.knob_radius: int = height
        self.knob_x: float = self._value_to_position(self.value)
        self.dragging: bool = False

    def _value_to_position(self, value: float) -> float:
        """
        Converts a slider value to a knob position.

        :param value: The value to convert.
        :return: The x-coordinate of the knob's position.
        """
        return self.rect.x + ((value - self.min_value) / (self.max_value - self.min_value)) * self.rect.width

    def _position_to_value(self, x: float) -> float:
        """
        Converts a knob position to a slider value.

        :param x: The x-coordinate of the knob's position.
        :return: The corresponding slider value.
        """
        relative_x = x - self.rect.x
        return max(self.min_value, min(self.max_value, (relative_x / self.rect.width) * (self.max_value - self.min_value)))

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles mouse events for the slider.

        :param event: The pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.position_in_element(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.action()
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_x = max(self.rect.x, min(self.rect.x + self.rect.width, event.pos[0]))
            self.value = self._position_to_value(self.knob_x)

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        # This method is overridden because hover behavior is not needed for this element.
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the slider on the screen.

        :param screen: The pygame.Surface to draw on.
        """
        # Draw the slider background
        pygame.draw.rect(screen, (180, 180, 180), self.rect, border_radius=self.rect.height // 2)

        # Draw the filled portion of the slider
        fill_width = int((self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, (255, 209, 0), fill_rect, border_radius=self.rect.height // 2)

        # Draw the slider border
        pygame.draw.rect(screen, (48, 55, 66), self.rect, width=2, border_radius=self.rect.height // 2)

    def action(self) -> None:
        """
        Defines the action to perform when the slider value changes.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the action method.")


class MusicVolumeSlider(Slider):
    """
    A slider for adjusting the music volume in the game.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        min_value: float = 0,
        max_value: float = 1,
    ):
        """
        Initializes the music volume slider.

        :param screen: The pygame.Surface where the slider will be drawn.
        :param x: The x-coordinate of the slider's position.
        :param y: The y-coordinate of the slider's position.
        :param width: The width of the slider.
        :param height: The height of the slider.
        :param min_value: The minimum value of the slider.
        :param max_value: The maximum value of the slider.
        :param initial_value: The initial value of the slider.
        """
        self.sound_manager: SoundManager = SoundManager()
        initial_value = self.sound_manager.get_music_volume()
        super().__init__(screen, x, y, width, height, min_value, max_value, initial_value)

    def action(self) -> None:
        """
        Updates the music volume based on the slider's value.
        """
        self.sound_manager.set_music_volume(self.value)


class SoundEffectsVolumeSlider(Slider):
    """
    A slider for adjusting the sound effects volume in the game.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        min_value: float = 0,
        max_value: float = 1,
    ):
        """
        Initializes the sound effects volume slider.

        :param screen: The pygame.Surface where the slider will be drawn.
        :param x: The x-coordinate of the slider's position.
        :param y: The y-coordinate of the slider's position.
        :param width: The width of the slider.
        :param height: The height of the slider.
        :param min_value: The minimum value of the slider.
        :param max_value: The maximum value of the slider.
        :param initial_value: The initial value of the slider.
        """
        self.sound_manager: SoundManager = SoundManager()
        initial_value = self.sound_manager.get_sound_volume()
        super().__init__(screen, x, y, width, height, min_value, max_value, initial_value)

    def action(self) -> None:
        """
        Updates the sound effects volume based on the slider's value.
        """
        self.sound_manager.set_sound_volume(self.value)
