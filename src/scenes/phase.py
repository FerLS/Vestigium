import pygame 

from scene import Scene

class Phase(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)

    def update(self, *args):
        raise NotImplementedError("Subclasses must implement this method")
    
    def events(self, events: list):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.finish_program()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.director.scene_manager.stack_scene("PauseMenu")

        self.pressed_keys = pygame.key.get_pressed()
    
    def draw(self):
        raise NotImplementedError("Subclasses must implement this method")