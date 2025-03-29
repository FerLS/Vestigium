import pygame


class Camera:
    """
    Represents a camera that follows a target (e.g., the player) and provides
    scrolling functionality for the game world. It defines view boundaries and
    handles offsets for rendering.
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initializes the camera.

        :param screen_width: The width of the screen in pixels.
        :param screen_height: The height of the screen in pixels.
        """
        self.scroll_x: float = 0  # Horizontal scroll offset
        self.scroll_y: float = 0  # Vertical scroll offset

        self.screen_width: int = screen_width
        self.screen_height: int = screen_height

        self.left_margin: int = screen_width // 4  # Left margin for horizontal scrolling
        self.right_margin: int = screen_width // 4  # Right margin for horizontal scrolling

        self.margin_y: int = screen_height // 4  # Margin for vertical scrolling

    def update(self, target_rect: pygame.Rect) -> None:
        """
        Updates the camera's position based on the target's position.

        :param target_rect: The pygame.Rect representing the target's position and size.
        """
        # Horizontal scrolling
        if target_rect.left < self.scroll_x + self.left_margin:
            self.scroll_x = target_rect.left - self.left_margin
        elif target_rect.right > self.scroll_x + self.screen_width - self.right_margin:
            self.scroll_x = target_rect.right - (self.screen_width - self.right_margin)

        # Vertical scrolling
        if target_rect.top < self.scroll_y + self.margin_y:
            self.scroll_y = target_rect.top - self.margin_y
        elif target_rect.bottom > self.scroll_y + self.screen_height - self.margin_y:
            self.scroll_y = target_rect.bottom - (self.screen_height - self.margin_y)

    def get_offset(self) -> tuple[int, int]:
        """
        Returns the current scroll offsets of the camera.

        :return: A tuple (scroll_x, scroll_y) representing the camera's offset.
        """
        return int(self.scroll_x), int(self.scroll_y)

    def get_horizontal_bounds(self) -> tuple[float, float]:
        """
        Returns the horizontal bounds of the camera's view.

        :return: A tuple (left_bound, right_bound) representing the horizontal bounds.
        """
        return self.scroll_x, self.scroll_x + self.screen_width

    def update_x_margin(self, new_left_margin: int, new_right_margin: int) -> None:
        """
        Updates the left and right margins for horizontal scrolling.

        :param new_left_margin: The new left margin in pixels.
        :param new_right_margin: The new right margin in pixels.
        """
        self.left_margin = new_left_margin
        self.right_margin = new_right_margin

    def get_view_rect(self) -> pygame.Rect:
        """
        Returns the view rectangle of the camera.

        :return: A pygame.Rect representing the camera's view area.
        """
        return pygame.Rect(self.scroll_x, self.scroll_y, self.screen_width, self.screen_height)

    def mask_from_rect(self, rect: pygame.Rect) -> pygame.mask.Mask:
        """
        Creates a mask from a given rectangle.

        :param rect: The pygame.Rect to create the mask from.
        :return: A pygame.mask.Mask object representing the mask of the rectangle.
        """
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        surface.fill((255, 255, 255, 255))  # Fill with white and full alpha
        return pygame.mask.from_surface(surface)

