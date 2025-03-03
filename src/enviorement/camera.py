import pygame

from utils.constants import CAMERA_LIMITS_X, CAMERA_LIMITS_Y, MAX_FALL_SPEED, MOVE_SPEED
from utils.juice import smooth_lerp  # Import smoothlerp


class Camera:
    def __init__(self):
        self.left_limit = CAMERA_LIMITS_X[0]
        self.right_limit = CAMERA_LIMITS_X[1]
        self.bottom_limit = CAMERA_LIMITS_Y[1]
        self.top_limit = CAMERA_LIMITS_Y[0]
        self.scroll_x = 0
        self.scroll_y = 0

    def update(self, player, keys):
        target_scroll_x = 0
        target_scroll_y = 0

        if player.rect.left < self.left_limit and keys[pygame.K_LEFT]:
            target_scroll_x = -MOVE_SPEED
        elif player.rect.right > self.right_limit and keys[pygame.K_RIGHT]:
            target_scroll_x = MOVE_SPEED

        if player.rect.top < self.top_limit:
            target_scroll_y = player.velocity_y

        if player.rect.bottom > self.bottom_limit:
            target_scroll_y = MAX_FALL_SPEED

        self.scroll_x = smooth_lerp(self.scroll_x, target_scroll_x, 0.25)
        self.scroll_y = target_scroll_y
