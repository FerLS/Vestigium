import pygame

from utils.constants import CAMERA_LIMITS_X, CAMERA_LIMITS_Y, MAX_FALL_SPEED, MOVE_SPEED


class Camera:
    def __init__(self):
        self.left_limit = CAMERA_LIMITS_X[0]
        self.right_limit = CAMERA_LIMITS_X[1]
        self.bottom_limit = CAMERA_LIMITS_Y[1]
        self.top_limit = CAMERA_LIMITS_Y[0]
        self.scroll_x = 0
        self.scroll_y = 0

    def update(self, player, keys):
        self.scroll_x = 0
        self.scroll_y = 0

        if player.rect.left < self.left_limit and keys[pygame.K_LEFT]:
            self.scroll_x = -MOVE_SPEED
        elif player.rect.right > self.right_limit and keys[pygame.K_RIGHT]:
            self.scroll_x = MOVE_SPEED

        if player.rect.top < self.top_limit:
            self.scroll_y = player.velocity_y

        if player.rect.bottom > self.bottom_limit:
            self.scroll_y = MAX_FALL_SPEED
