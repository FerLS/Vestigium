import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import NewGameText, OptionsText, ExitText, ContinueText
from utils.constants import WIDTH, HEIGHT

class StartScreen(GUIScreen):
    def __init__(self, menu, image_path):
        GUIScreen.__init__(self, menu, image_path)
        self.gui_elements.append(NewGameText(self, (WIDTH//2 - 75, 350)))
        self.gui_elements.append(OptionsText(self, (WIDTH//2 - 65, 400)))
        self.gui_elements.append(ExitText(self, (WIDTH//2 - 50, 450)))        
        