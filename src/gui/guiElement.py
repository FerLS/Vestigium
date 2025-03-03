import pygame 
from abc import ABC

class GUIElement(ABC):
    def __init__(self, screen, rect):
        self.screen = screen
        self.rect = rect # To know if click was pressed

    # Locate the element in the screen  
    def set_position(self, position): 
        posx, posy = position
        self.rect.x = posx
        self.rect.y = posy

    # Know if it was clicked
    def position_in_element(self, position):
        posx, posy = position
        if (posx >= self.rect.left) and (posx <= self.rect.right) \
        and (posy >= self.rect.top) and (posy <= self.rect.bottom):
            return True
        else:
            return False
        
    def draw(self):
        raise NotImplementedError('Draw method must be implemented in subclass')
    
    def action(self):
        raise NotImplementedError('Action method must be implemented in subclass')
        
