import pygame
from managers.resource_manager import ResourceManager


class KeyItem(pygame.sprite.Sprite):
    """
    Represents a collectible key item in the game. The key can be picked up by the player
    when they collide with it.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes the key item.

        :param x: The x-coordinate of the key's position.
        :param y: The y-coordinate of the key's position.
        """
        super().__init__()
        self.resource_manager: ResourceManager = ResourceManager()

        self.image: pygame.Surface = self.resource_manager.load_image("key.png", "assets\\images")
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() // 3, self.image.get_height() // 3)
        )
        self.image = pygame.transform.rotate(self.image, 270)  # Rotate the image 270 degrees

        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))

        self.picked: bool = False

    def update(self, player: pygame.sprite.Sprite) -> None:
        """
        Updates the key's state by checking for collision with the player.

        :param player: The player object to check for collision.
        """
        if self.rect.colliderect(player.rect):
            self.picked = True

    def draw(self, screen: pygame.Surface, offset: tuple[int, int]) -> None:
        """
        Draws the key on the screen if it has not been picked up.

        :param screen: The pygame.Surface to draw on.
        :param offset: The camera offset for rendering.
        """
        if self.picked:
            return  # Do not draw the key if it has been picked up

        offset_x, offset_y = offset
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
