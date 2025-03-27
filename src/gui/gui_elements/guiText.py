import pygame
from gui.guiElement import GUIElement
from resource_manager import ResourceManager


class TextGUI(GUIElement):
    def __init__(self, screen, font, color, text, position):
        self.font = font
        self.base_color = color
        self.hover_color = (
            255,
            255,
            255,
        )  # <- Cambia esto si quieres otro color al pasar el mouse
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
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "New Game", position)

    def action(self):
        self.screen.menu.play_game()


class ExitText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Exit", position)

    def action(self):
        self.screen.menu.exit_game()


class OptionsText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Options", position)

    def action(self):
        self.screen.menu.show_options_screen()


class GoBackText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Go Back", position)

    def action(self):
        self.screen.menu.return_previous_scene()


class MusicVolumeText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Music", position)

    def action(self):
        pass


class SoundEffectsVolumeText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Sound Effects", position)

    def action(self):
        pass


# Pause menu text
class ContinueText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Continue", position)

    def action(self):
        self.screen.menu.continue_game()


class GoToMainMenuText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Main Menu", position)

    def action(self):
        self.screen.menu.go_to_main_menu()


# Die menu text
class YouDiedText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "YOU DIED", position)

    def action(self):
        pass

    def update_hover(self, mouse_pos):
        pass


class RestartLevel(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Restart", position)

    def action(self):
        self.screen.menu.restart_level()


# Tutorial text
class InitialInstructionText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        self.lines = [
            font.render(
                "use LEFT and RIGHT to move and UP to jump", True, (255, 255, 255)
            ),
            font.render("but be careful with the lights...", True, (255, 255, 255)),
        ]
        self.line_spacing = 5  # Space between lines
        self.rects = [line.get_rect() for line in self.lines]
        self.set_position(position)

    def set_position(self, position):
        # Adjust positions for each line
        for i, rect in enumerate(self.rects):
            rect.topleft = (
                position[0],
                position[1] + i * (rect.height + self.line_spacing),
            )

    def draw(self, screen):
        for line, rect in zip(self.lines, self.rects):
            screen.blit(line, rect)


class RetryInstructionText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        self.lines = [
            font.render("lets try again-", True, (255, 255, 255)),
            font.render("this time be more careful", True, (255, 255, 255)),
        ]
        self.line_spacing = 5  # Space between lines
        self.rects = [line.get_rect() for line in self.lines]
        self.set_position(position)

    def set_position(self, position):
        # Adjust positions for each line
        for i, rect in enumerate(self.rects):
            rect.topleft = (
                position[0],
                position[1] + i * (rect.height + self.line_spacing),
            )

    def draw(self, screen):
        for line, rect in zip(self.lines, self.rects):
            screen.blit(line, rect)


class GlideInstructionText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(
            self,
            screen,
            font,
            (255, 255, 255),
            "while falling, press SPACE to glide",
            position,
        )

    def action(self):
        pass


class SwimInstructionText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(
            self,
            screen,
            font,
            (255, 255, 255),
            "use LEFT, RIGHT, UP and DOWN to swim",
            position,
        )

    def action(self):
        pass


class BossTutorial(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(
            self,
            screen,
            font,
            (255, 255, 255),
            "Be careful, hide from the light!",
            position,
        )

    def action(self):
        pass
