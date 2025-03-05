import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import MusicVolumeText, SoundEffectsVolumeText, GoBackText

class OptionsScreen(GUIScreen):
    def __init__(self, menu, image_name):
        GUIScreen.__init__(self, menu, image_name)
        self.gui_elements.append(GoBackText(self, (100, 100)))
        self.gui_elements.append(MusicVolumeText(self, (200, 200)))
        self.gui_elements.append(SoundEffectsVolumeText(self, (200, 300)))