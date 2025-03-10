import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import NewGameText, OptionsText, ExitText, ContinueText
from utils.constants import WIDTH, HEIGHT

class StartScreen(GUIScreen):
    def __init__(self, menu, image_name):
        GUIScreen.__init__(self, menu, image_name)
        self.gui_elements.append(NewGameText(self, (200, 200)))
        self.gui_elements.append(OptionsText(self, (200, 300)))
        self.gui_elements.append(ExitText(self, (200, 400)))

        