import pygame

from utils.constants import WIDTH, HEIGHT
from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import ContinueText, OptionsText, GoToMainMenuText, RestartLevel

class PauseScreen(GUIScreen):
    def __init__(self, menu, image_path):
        GUIScreen.__init__(self, menu, image_path)
        self.gui_elements.append(ContinueText(self, (WIDTH//2 - 75, 360)))
        self.gui_elements.append(RestartLevel(self, (WIDTH//2 - 67, 400)))
        self.gui_elements.append(OptionsText(self, (WIDTH//2 - 67, 440)))
        self.gui_elements.append(GoToMainMenuText(self, (WIDTH//2 - 83, 480)))

        