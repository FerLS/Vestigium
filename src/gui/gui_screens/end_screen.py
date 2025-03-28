import pygame
from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import EndOfGameText, FinalText, GoToMainMenuText
from utils.constants import WIDTH, HEIGHT

class EndScreen(GUIScreen):
    def __init__(self, menu):
        self.menu = menu
        self.image = None
        self.gui_elements = []
        
        self.gui_elements.append(FinalText(self, (100, 100)))
        self.gui_elements.append(EndOfGameText(self, (WIDTH/2 - 50, HEIGHT/1.5)))
        self.gui_elements.append(GoToMainMenuText(self, (WIDTH/2 - 65, HEIGHT/1.2)))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for element in self.gui_elements:
            element.update_hover(mouse_pos)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for element in self.gui_elements:
            element.draw(screen)

    def events(self, event_list):
        for event in event_list:
            for element in self.gui_elements:
                element.handle_event(event)