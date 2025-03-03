import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiButton import PlayButton

class ConfigScreen(GUIScreen):
    def __init__(self, menu, image_name):
        GUIScreen.__init__(self, menu, image_name)
        self.gui_elements = []
        self.gui_elements.append(PlayButton(self, (200, 200)))