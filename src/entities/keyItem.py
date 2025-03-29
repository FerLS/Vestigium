import pygame
from resource_manager import ResourceManager


class KeyItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.resource_manager = ResourceManager()
        self.image = self.resource_manager.load_image("key.png", "assets\\images")
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width() // 3, self.image.get_height() // 3)
        )
        self.image = pygame.transform.rotate(
            self.image, 270
        )  # Rotate the image 270 degrees (90 + 180)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.picked = False

    def update(self, player):
        # Check collision with the player
        if self.rect.colliderect(player.rect):
            self.picked = True

    def draw(self, screen, offset):

        if self.picked:
            return
        offset_x, offset_y = offset
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
