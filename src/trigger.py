import pygame
from gui.gui_elements.guiText import GlideInstructionText

class Trigger:
    def __init__(self, rect, action, triggered_once=True):
        self.rect = rect  
        self.action = action 
        self.triggered_once = triggered_once
        self.triggered = False

    def check(self, player_rect):
        if self.rect.colliderect(player_rect) and (not self.triggered or not self.triggered_once):
            text = self.action()
            self.triggered = True
            return text

# Actions that can be triggered by a Trigger
def show_glide_message(screen, player):
    print("ejecuto")
    text = GlideInstructionText(screen, (100, 100))
    player.can_glide = True
    return text
