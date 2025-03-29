import pygame

from gui.gui_screen import GUIScreen
from gui.gui_elements.gui_text import MusicVolumeText, SoundEffectsVolumeText,GoBackText
from gui.gui_elements.gui_slider import MusicVolumeSlider, SoundEffectsVolumeSlider
from utils.constants import WIDTH

class OptionsScreen(GUIScreen):
    def __init__(self, menu, image_path):
        GUIScreen.__init__(self, menu, image_path)

    def _init_gui_elements(self):
        gui_elements = []   
        gui_elements.append(MusicVolumeText(self, (WIDTH//2 - 50, 360)))
        gui_elements.append(MusicVolumeSlider(self, WIDTH//2 - 75, 390, 125, 10))
        gui_elements.append(SoundEffectsVolumeText(self, (WIDTH//2 - 120, 420)))
        gui_elements.append(SoundEffectsVolumeSlider(self, WIDTH//2 - 75, 450, 125, 10))
        gui_elements.append(GoBackText(self, (WIDTH//2 - 70, 500)))
        return gui_elements

    def events(self, event_list):
        for event in event_list:
            for element in self.gui_elements:
                element.handle_event(event)
