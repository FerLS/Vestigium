import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import ContinueText, OptionsText, GoToMainMenuText, RestartLevel

class PauseScreen(GUIScreen):
    def __init__(self, menu, image_path):
        GUIScreen.__init__(self, menu, image_path)
        self.gui_elements.append(ContinueText(self, (200, 200)))
        self.gui_elements.append(RestartLevel(self, (200, 300)))
        self.gui_elements.append(OptionsText(self, (200, 400)))
        self.gui_elements.append(GoToMainMenuText(self, (200, 500)))

        