import pygame 
import os

from abc import ABC
from managers.resource_manager import ResourceManager
from utils.constants import WIDTH, HEIGHT

class GUIScreen(ABC):
    def __init__(self, menu, images_path):
        self.menu = menu
        self.images = self._init_images(images_path)
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.frame_counter = 0
        self.gui_elements = self._init_gui_elements()

    def _init_gui_elements(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def _init_images(self, images_path):
        images = []
        for file in os.listdir(images_path):
                if file.endswith(".png"):
                    image = ResourceManager().load_image(file, images_path)
                    scaled_image = pygame.transform.scale(image, (WIDTH, HEIGHT))
                    images.append(scaled_image)
        return images

    def update(self):
        self.frame_counter = (self.frame_counter + 1) % 15
        if self.frame_counter == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]

        mouse_pos = pygame.mouse.get_pos()
        for element in self.gui_elements:
            element.update_hover(mouse_pos)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        for element in self.gui_elements:
            element.draw(screen)

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