import pygame 

from gui.guiElement import GUIElement
from resource_manager import ResourceManager

class GUIButton(GUIElement):
    def __init__(self, screen, image_name, position):
        self.image = ResourceManager().load_image(image_name, "assets\\images\\gui")
        # TODO: Check this size
        self.image = pygame.transform.scale(self.image, (100, 50))
        GUIElement.__init__(self, screen, self.image.get_rect())
        self.set_position(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PlayButton(GUIButton):
    def __init__(self, screen, position):
        GUIButton.__init__(self, screen, "play_button.png", position)

    def action(self):
        self.screen.menu.play_game()

class ConfigButton(GUIButton):
    def __init__(self, screen, position):
        GUIButton.__init__(self, screen, "play_button.png", position)

    def action(self):
        self.screen.menu.show_config_screen()
    
class ExitButton(GUIButton):
    def __init__(self, screen, position):
        GUIButton.__init__(self, screen, "play_button.png", position)

    def action(self):
        self.screen.menu.exit_game()

