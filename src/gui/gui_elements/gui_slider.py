import pygame
from abc import ABC
from gui.guiElement import GUIElement
from sound_manager import SoundManager  

class Slider(GUIElement):
    def __init__(self, screen, x, y, width, height, min_value=0, max_value=1, initial_value=0.5):
        super().__init__(screen, pygame.Rect(x, y, width, height)) 
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value  
        self.knob_radius = height
        self.knob_x = self._value_to_position(self.value)
        self.dragging = False

    def _value_to_position(self, value):
        return self.rect.x + ((value - self.min_value) / (self.max_value - self.min_value)) * self.rect.width

    def _position_to_value(self, x):
        relative_x = x - self.rect.x
        return max(self.min_value, min(self.max_value, (relative_x / self.rect.width) * (self.max_value - self.min_value)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.position_in_element(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.action()   
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_x = max(self.rect.x, min(self.rect.x + self.rect.width, event.pos[0]))
            self.value = self._position_to_value(self.knob_x)

    def update_hover(self, mouse_pos):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (180, 180, 180), self.rect, border_radius=self.rect.height // 2)

        fill_width = int((self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, (255, 209, 0), fill_rect, border_radius=self.rect.height // 2)

        pygame.draw.rect(screen, (48, 55, 66), self.rect, width=2, border_radius=self.rect.height // 2)


class MusicVolumeSlider(Slider):
    def __init__(self, screen, x, y, width, height, min_value=0, max_value=1, initial_value=0.5):
        self.sound_manager = SoundManager()
        initial_value = self.sound_manager.get_music_volume()   
        super().__init__(screen, x, y, width, height, min_value, max_value, initial_value)
        
    def action(self):
        self.sound_manager.set_music_volume(self.value)

class SoundEffectsVolumeSlider(Slider):
    def __init__(self, screen, x, y, width, height, min_value=0, max_value=1, initial_value=0.5):
        self.sound_manager = SoundManager()
        initial_value = self.sound_manager.get_sound_volume()   
        super().__init__(screen, x, y, width, height, min_value, max_value, initial_value)

    def action(self):
        self.sound_manager.set_sound_volume(self.value)

