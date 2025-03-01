import pygame

from utils.constants import MovementDirections

class Light:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_threshold(self.image, (255, 255, 255, 255), (50, 50, 50, 255))

    def update_position(self, gravedigger):
        if gravedigger.movement == MovementDirections.LEFT:
            self.rect.topleft = (gravedigger.rect.x - 25, gravedigger.rect.y + 2)
        else:
            self.rect.topleft = (gravedigger.rect.x + 10, gravedigger.rect.y + 2)

    def collide(self, player, gravedigger):
        offset_x = player.rect.x - self.rect.x
        offset_y = player.rect.y - self.rect.y
        if self.mask.overlap(player.mask, (offset_x, offset_y)):
            player.die()
            gravedigger.stop()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)