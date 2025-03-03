import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiButton import PlayButton, ConfigButton, ExitButton

class StartScreen(GUIScreen):
    def __init__(self, menu, image_name):
        GUIScreen.__init__(self, menu, image_name)
        self.gui_elements.append(PlayButton(self, (200, 200)))
        self.gui_elements.append(ConfigButton(self, (200, 300)))
        self.gui_elements.append(ExitButton(self, (200, 400)))


        