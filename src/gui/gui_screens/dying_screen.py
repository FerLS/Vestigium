import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import YouDiedText, RestartLevel, GoToMainMenuText
from utils.constants import WIDTH

class DyingScreen(GUIScreen):
    def __init__(self, menu, image_path):
        GUIScreen.__init__(self, menu, image_path)
        self.gui_elements.append(YouDiedText(self, (WIDTH//2 - 70, 400)))
        self.gui_elements.append(RestartLevel(self, (WIDTH//2 - 65, 440)))
        self.gui_elements.append(GoToMainMenuText(self, (WIDTH//2 - 75, 480)))
