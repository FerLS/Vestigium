import pygame 

from scene import Scene

class Menu(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)

    def update(self, *args):
        raise NotImplementedError("Subclasses must implement this method")
    
    def events(self, events: list):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.finish_program()
        self.screen_list[-1].events(events)
    
    def draw(self):
        self.screen_list[-1].draw(self.director.screen)