import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import YouDiedText, RestartLevel, GoToMainMenuText

class DyingScreen(GUIScreen):
    def __init__(self, menu, image_path):
        GUIScreen.__init__(self, menu, image_path)
        self.gui_elements.append(YouDiedText(self, (200, 200)))
        self.gui_elements.append(RestartLevel(self, (200, 300)))
        self.gui_elements.append(GoToMainMenuText(self, (200, 400)))
