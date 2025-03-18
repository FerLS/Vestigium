import pygame
from gui.gui_elements.guiText import GlideInstructionText

class Trigger:
    def __init__(self, rect, action, triggered_once=True):
        self.rect = rect  
        self.action = action 
        self.triggered_once = triggered_once
        self.triggered = False
        self.text = None

    def check(self, player_rect):
        if self.rect.colliderect(player_rect) and (not self.triggered or not self.triggered_once):
            text = self.action()
            self.triggered = True
            self.text = text
    
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
