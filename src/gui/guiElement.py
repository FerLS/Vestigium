import pygame 
from abc import ABC

class GUIElement(ABC):
    def __init__(self, screen, rect):
        self.screen = screen
        self.rect = rect # To know if click was pressed
        self.clicked = False

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
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = False
                if self.position_in_element(event.pos):
                    self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.position_in_element(event.pos):
                if self.clicked:
                    self.action()
        
    def draw(self):
        raise NotImplementedError('Draw method must be implemented in subclass')
    
    def action(self):
        raise NotImplementedError('Action method must be implemented in subclass')
    
    
