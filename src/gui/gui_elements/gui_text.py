import pygame
from gui.gui_element import GUIElement
from managers.resource_manager import ResourceManager

# Constants for colors
BASE_COLOR = (255, 209, 0)
HOVER_COLOR = (255, 255, 255)
FINAL_TEXT_COLOR = (255, 255, 255)

# Constants for font size
FONT_SIZE = 20

# Constants for file paths
FONT_PATH = "assets\\fonts"
FONT_NAME = "Commodore-64-v621c.TTF"

# Constants for sound paths
HOVER_SOUND = "hover.wav"
CLICK_SOUND = "click.wav"
SOUND_PATH = "assets\\sounds"

class TextGUI(GUIElement):
    """
    Represents a text-based GUI element. Handles rendering text, hover effects, and actions.
    """

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, color: tuple[int, int, int], text: str, position: tuple[int, int]):
        """
        Initializes the text-based GUI element.

        :param screen: The pygame.Surface where the element will be drawn.
        :param font: The font used to render the text.
        :param color: The base color of the text.
        :param text: The text content to display.
        :param position: The (x, y) position of the text on the screen.
        """
        self.font: pygame.font.Font = font
        self.base_color: tuple[int, int, int] = color
        self.hover_color: tuple[int, int, int] = HOVER_COLOR
        self.text: str = text
        self.color: tuple[int, int, int] = color

        self.lines: list[str] = text.split("\n")
        self.images: list[pygame.Surface] = [font.render(line.strip(), True, color) for line in self.lines]

        width: int = max(img.get_width() for img in self.images)
        height: int = sum(img.get_height() for img in self.images)

        super().__init__(screen, pygame.Rect(position[0], position[1], width, height))
        self.set_position(position)

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        """
        Updates the hover state of the text element based on the mouse position.

        :param mouse_pos: The (x, y) position of the mouse.
        """
        super().update_hover(mouse_pos)
        color = self.hover_color if self.hovered else self.base_color
        self.images = [self.font.render(line.strip(), True, color) for line in self.lines]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the text element on the screen.

        :param screen: The pygame.Surface to draw on.
        """
        y_offset = 1
        for img in self.images:
            screen.blit(img, (self.rect.x, self.rect.y + y_offset))
            y_offset += img.get_height()

    def action(self) -> None:
        """
        Defines the action to perform when the text element is clicked.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the action method.")

class NewGameText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, BASE_COLOR, "New Game", position)

    def action(self):
        self.screen.menu.play_game()

class ExitText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, BASE_COLOR, "Exit", position)

    def action(self):
        self.screen.menu.exit_game()

class OptionsText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, BASE_COLOR, "Options", position)

    def action(self):
        self.screen.menu.show_options_screen()

class GoBackText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, BASE_COLOR, "Go Back", position)

    def action(self):
        self.screen.menu.return_previous_scene()

class MusicVolumeText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, BASE_COLOR, "Music", position)

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

    def update_hover(self, mouse_pos):
        # This method is overridden because hover behavior is not needed for this element.
        pass


class SoundEffectsVolumeText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, BASE_COLOR, "Sound Effects", position)

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

    def update_hover(self, mouse_pos):
        # This method is overridden because hover behavior is not needed for this element.
        pass


# Pause menu text
class ContinueText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, BASE_COLOR, "Continue", position)

    def action(self):
        self.screen.menu.continue_game()

class GoToMainMenuText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, BASE_COLOR, "Main Menu", position)

    def action(self):
        self.screen.menu.go_to_main_menu()

# Die menu text
class YouDiedText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, BASE_COLOR, "YOU DIED", position)

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

    def update_hover(self, mouse_pos):
        # This method is overridden because hover behavior is not needed for this element.
        pass


class RestartLevel(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, BASE_COLOR, "Restart", position)

    def action(self):
        self.screen.menu.restart_level()

class GlideInstructionText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(
            self,
            screen,
            font,
            FINAL_TEXT_COLOR,
            "while falling, press SPACE to glide",
            position,
        )

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass


class SwimInstructionText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(
            self,
            screen,
            font,
            FINAL_TEXT_COLOR,
            "use LEFT, RIGHT, UP and DOWN to swim",
            position,
        )

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass


class BossTutorialText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(
            self,
            screen,
            font,
            FINAL_TEXT_COLOR,
            """find the gravedigger's key! 
            but be careful, hide behind the walls!""",
            position,
        )

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

class BossStairsText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(
            self,
            screen,
            font,
            FINAL_TEXT_COLOR,
            """use UP to climb the stairs""",
            position,
        )

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

class DoorText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(
            self,
            screen,
            font,
            FINAL_TEXT_COLOR,
            "you need to find the key to open the gate!",
            position,
        )

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

class KeyText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(
            self,
            screen,
            font,
            FINAL_TEXT_COLOR,
            "now that you have the key, you can open the door!",
            position,
        )

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

class FinalText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        final_text = """It rose from the still waters, 
        like an echo no longer afraid to be forgotten.
        The light found it first... and it didn't run.

        No bodies left to haunt, 
        no shadows left to hide in. 
        Only the worldalive, radiant, 
        beautifully indifferent.

        And in that final moment, 
        it chose to dissolve.
        Not in defeat. In peace.

        It became mist, a silhouette among branches, 
        a natural shadow.

        Free, at last."""
        TextGUI.__init__(self, screen, font, FINAL_TEXT_COLOR, final_text, position)

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

    def update_hover(self, mouse_pos):
        # This method is overridden because hover behavior is not needed for this element.
        pass


class EndOfGameText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        TextGUI.__init__(self, screen, font, FINAL_TEXT_COLOR, "The End", position)

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

    def update_hover(self, mouse_pos):
        # This method is overridden because hover behavior is not needed for this element.
        pass


class InitialInstructionText(TextGUI):
    def __init__(self, screen, position, time=10):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        text = """use LEFT and RIGHT to move and SPACE to jump...
        but be careful with the lights!"""
        TextGUI.__init__(self, screen, font, FINAL_TEXT_COLOR, text, position)
        self.time = time
        self.visible = False

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

    def update_hover(self, mouse_pos):
        # This method is overridden because hover behavior is not needed for this element.
        pass

    def draw(self, screen):
        if self.visible:
            super().draw(screen)

    def update(self, dt):
        self.time -= dt
        if self.time <= 0:
            self.visible = False
            self.time = 0
            
class RetryInstructionText(TextGUI):
    def __init__(self, screen, position, time=5):
        font = ResourceManager().load_font(FONT_NAME, FONT_PATH, FONT_SIZE)
        text = """lets try again, 
        this time be more careful"""
        TextGUI.__init__(self, screen, font, FINAL_TEXT_COLOR, text, position)
        self.time = time
        self.visible = True

    def action(self):
        # This method is overridden because no specific action is required when clicked.
        pass

    def update_hover(self, mouse_pos):
        # This method is overridden because hover behavior is not needed for this element.
        pass

    def draw(self, screen):
        if self.visible:
            super().draw(screen)

    def update(self, dt):
        self.time -= dt
        if self.time <= 0:
            self.visible = False
            self.time = 0