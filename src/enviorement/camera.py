import pygame

from utils.constants import CAMERA_LIMITS, MOVE_SPEED


class Camera:
    def __init__(
        self,
    ):
        self.left_limit = CAMERA_LIMITS[0]
        self.right_limit = CAMERA_LIMITS[1]
        self.scroll = 0

    def update(self, player_rect, keys):
        if player_rect.left < self.left_limit and keys[pygame.K_LEFT]:
            self.scroll = -MOVE_SPEED
        elif player_rect.right > self.right_limit and keys[pygame.K_RIGHT]:
            self.scroll = MOVE_SPEED
        else:
            self.scroll = 0
