import pygame

from gui.guiScreen import GUIScreen
from gui.gui_elements.guiText import NewGameText, OptionsText, ExitText, ContinueText
from utils.constants import WIDTH, HEIGHT

class StartScreen(GUIScreen):
    def __init__(self, menu, image_path):
        GUIScreen.__init__(self, menu, image_path)
        self.gui_elements.append(NewGameText(self, (WIDTH//2 - 75, 400)))
        self.gui_elements.append(OptionsText(self, (WIDTH//2 - 71, 440)))
        self.gui_elements.append(ExitText(self, (WIDTH//2 - 55, 480))) 
               
    def events(self, event_list):
        for event in event_list:
            for element in self.gui_elements:
                element.handle_event(event)