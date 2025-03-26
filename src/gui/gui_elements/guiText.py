import pygame
from gui.guiElement import GUIElement
from resource_manager import ResourceManager
from sound_manager import SoundManager

class TextGUI(GUIElement):
    def __init__(self, screen, font, color, text, position):
        self.font = font
        self.base_color = color
        self.hover_color = (255, 255, 255)  # <- Cambia esto si quieres otro color al pasar el mouse
        self.text = text
        self.image = font.render(text, True, color)
        GUIElement.__init__(self, screen, self.image.get_rect())
        self.set_position(position)
        

    def update_hover(self, mouse_pos):
        super().update_hover(mouse_pos)
        if self.hovered:
            self.image = self.font.render(self.text, True, self.hover_color)
        else:
            self.image = self.font.render(self.text, True, self.base_color)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
# Start screen text
class NewGameText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets\\fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 209, 0), "New Game", position)

    def action(self):
       self.screen.menu.play_game()

class ExitText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets\\fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Exit", position)
    
    def action(self):
        self.screen.menu.exit_game()

class OptionsText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets\\fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Options", position)

    def action(self):
        self.screen.menu.show_options_screen()

class GoBackText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets\\fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Go Back", position)

    def action(self):
        self.screen.menu.return_previous_scene()

class MusicVolumeText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets\\fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Music", position)

    def action(self):
        pass

    def update_hover(self, mouse_pos):
        pass

class SoundEffectsVolumeText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets\\fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Sound Effects", position)

    def action(self):
        pass

    def update_hover(self, mouse_pos):
        pass

# Pause menu text
class ContinueText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets\\fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Continue", position)

    def action(self):
        self.screen.menu.continue_game()

class GoToMainMenuText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets\\fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Main Menu", position)

    def action(self):
        self.screen.menu.go_to_main_menu()

# Die menu text
class YouDiedText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets\\fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 209, 0), "YOU DIED", position)

    def action(self):
        pass

    def update_hover(self, mouse_pos):
        pass

class RestartLevel(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets\\fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Restart", position)

    def action(self):
        self.screen.menu.restart_level()

# Tutorial text
class GlideInstructionText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 255, 255), "while falling, press SPACE to glide", position)

    def action(self):
        pass

class SwimInstructionText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 255, 255), "use LEFT, RIGHT, UP and DOWN to swim", position)

    def action(self):
        pass