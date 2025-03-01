from abc import ABC

from enviorement.tilemap import Tilemap

class Scene(ABC):
    def __init__(self, director, screen):
        self.director = director
        self.screen = screen

    def update(self, *args):
        raise NotImplementedError("Subclasses must implement this method")
    
    def events(self, *args):
        raise NotImplementedError("Subclasses must implement this method")
    
    def draw(self):
        raise NotImplementedError("Subclasses must implement this method")