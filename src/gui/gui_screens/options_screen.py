import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import MusicVolumeText, SoundEffectsVolumeText, GoBackText
from gui.gui_elements.gui_slider import MusicVolumeSlider

class OptionsScreen(GUIScreen):
    def __init__(self, menu, image_path):
        GUIScreen.__init__(self, menu, image_path)
        self.gui_elements.append(GoBackText(self, (100, 100)))
        self.gui_elements.append(MusicVolumeText(self, (200, 200)))
        self.gui_elements.append(MusicVolumeSlider(self, 400, 200, 300, 8))
        self.gui_elements.append(SoundEffectsVolumeText(self, (200, 300)))

    def events(self, event_list):
        for event in event_list:
            for element in self.gui_elements:
                element.handle_event(event)
