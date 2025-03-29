import pygame 

from scenes.scene import Scene
from gui.gui_screen import GUIScreen
from managers.sound_manager import SoundManager

class Menu(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        self.screen_list: list[GUIScreen] = []
        self.sound_manager: SoundManager = SoundManager()

    def update(self):
        self.screen_list[-1].update()
    
    def events(self, events: list):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.finish_program()
        self.screen_list[-1].events(events)
    
    def draw(self):
        self.screen_list[-1].draw(self.director.screen)
    
    def continue_procedure(self):
        pass