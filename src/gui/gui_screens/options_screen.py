import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import MusicVolumeText, SoundEffectsVolumeText, GoBackText
from gui.gui_elements.gui_slider import MusicVolumeSlider
from utils.constants import WIDTH

class OptionsScreen(GUIScreen):
    def __init__(self, menu, image_path):
        GUIScreen.__init__(self, menu, image_path)
        self.gui_elements.append(MusicVolumeText(self, (WIDTH//2 - 50, 360)))
        self.gui_elements.append(MusicVolumeSlider(self, WIDTH//2 - 75, 390, 125, 10))
        self.gui_elements.append(SoundEffectsVolumeText(self, (WIDTH//2 - 120, 420)))
        self.gui_elements.append(GoBackText(self, (WIDTH//2 - 70, 480)))


    def events(self, event_list):
        for event in event_list:
            for element in self.gui_elements:
                element.handle_event(event)
