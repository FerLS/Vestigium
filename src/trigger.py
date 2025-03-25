import math

import pygame

from gui.gui_elements.guiText import GlideInstructionText, SwimInstructionText
from light2 import ConeLight
from utils.constants import SCALE_FACTOR, WIDTH, HEIGHT


class Trigger:
    def __init__(self, rect, action, triggered_once=True, display_time=3):
        self.rect = rect  
        self.action = action 
        self.triggered_once = triggered_once
        self.triggered = False

        self.text = None
        self.display_time = display_time  
        self.current_time = 0 

    def check(self, player_rect):
        if self.rect.colliderect(player_rect) and (not self.triggered or not self.triggered_once):
            self.text = self.action()
            self.triggered = True
            self.current_time = self.display_time  

    def update(self, dt):
        if self.text is not None and self.current_time > 0:
            self.current_time -= dt
            if self.current_time <= 0:
                self.text = None  

    def draw(self, screen):
        if self.text is not None:
            self.text.draw(screen)

# Actions that can be triggered by a Trigger
def glide(screen, player):
    text = GlideInstructionText(screen, (100, 100))
    player.can_glide = True
    return text

def change_camera_y_margin(camera, new_margin):
    camera.margin_y = new_margin
    return None


def change_scene(director, scene):
    print("Changing scene to", scene)
    director.scene_manager.change_scene(scene)
    return None