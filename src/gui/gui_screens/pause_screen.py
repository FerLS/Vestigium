import pygame

from utils.constants import WIDTH, HEIGHT
from gui.gui_screen import GUIScreen
from gui.gui_elements.gui_text import ContinueText, OptionsText, GoToMainMenuText, RestartLevel

class PauseScreen(GUIScreen):
    def __init__(self, menu, image_path):
        GUIScreen.__init__(self, menu, image_path)

    def _init_gui_elements(self):
        gui_elements = []
        gui_elements.append(ContinueText(self, (WIDTH//2 - 75, 360)))
        gui_elements.append(RestartLevel(self, (WIDTH//2 - 67, 400)))
        gui_elements.append(OptionsText(self, (WIDTH//2 - 67, 440)))
        gui_elements.append(GoToMainMenuText(self, (WIDTH//2 - 83, 480)))
        return gui_elements

    def events(self, event_list):
        for event in event_list:
            for element in self.gui_elements:
                element.handle_event(event)   