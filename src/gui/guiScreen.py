import pygame 

from abc import ABC
from resource_manager import ResourceManager
from utils.constants import WIDTH, HEIGHT


class GUIScreen(ABC):
    def __init__(self, menu, image_name):
        self.menu = menu
        self.image = ResourceManager().load_image(image_name, "assets\\images\\gui")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.gui_elements = []

    def events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked_element = None
                for element in self.gui_elements:
                    if element.position_in_element(event.pos):
                        self.clicked_element = element
            if event.type == pygame.MOUSEBUTTONUP:
                for element in self.gui_elements:
                    if element.position_in_element(event.pos):
                        if element == self.clicked_element:
                            element.action()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        for element in self.gui_elements:
            element.draw(screen)