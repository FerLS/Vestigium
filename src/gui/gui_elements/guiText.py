import pygame
from gui.guiElement import GUIElement
from resource_manager import ResourceManager
from sound_manager import SoundManager

class TextGUI(GUIElement):
    def __init__(self, screen, font, color, text, position):
        self.font = font
        self.base_color = color
        self.hover_color = (255, 255, 255)
        self.text = text
        self.color = color

        self.lines = text.split("\n")
        self.images = [font.render(line.strip(), True, color) for line in self.lines]

        width = max(img.get_width() for img in self.images)
        height = sum(img.get_height() for img in self.images)

        GUIElement.__init__(self, screen, pygame.Rect(position[0], position[1], width, height))
        self.set_position(position)

    def update_hover(self, mouse_pos):
        super().update_hover(mouse_pos)
        color = self.hover_color if self.hovered else self.base_color
        self.images = [self.font.render(line.strip(), True, color) for line in self.lines]

    def draw(self, screen):
        y_offset = 1
        for img in self.images:
            screen.blit(img, (self.rect.x, self.rect.y + y_offset))
            y_offset += img.get_height()
    
    
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

    def update_hover(self, mouse_pos):
        pass

class SoundEffectsVolumeText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font(
            "Commodore-64-v621c.TTF", "assets\\fonts", 20
        )
        TextGUI.__init__(self, screen, font, (255, 209, 0), "Sound Effects", position)

    def action(self):
        pass

    def update_hover(self, mouse_pos):
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


class BossTutorialText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(
            self,
            screen,
            font,
            (255, 255, 255),
            """find the gravedigger's key! 
            but be careful, hide behind the walls!""",
            position,
        )

    def action(self):
        pass

class BossStairsText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(
            self,
            screen,
            font,
            (255, 255, 255),
            """use UP to climb the stairs""",
            position,
        )

    def action(self):
        pass
class DoorText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(
            self,
            screen,
            font,
            (255, 255, 255),
            "you need to find the key to open the gate!",
            position,
        )

    def action(self):
        pass

class KeyText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(
            self,
            screen,
            font,
            (255, 255, 255),
            "now that you have the key, you can open the door!",
            position,
        )

    def action(self):
        pass

# Final screen text
class FinalText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
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
        TextGUI.__init__(self, screen, font, (255, 255, 255), final_text, position)

    def action(self):
        pass

    def update_hover(self, mouse_pos):
        pass

class EndOfGameText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(self, screen, font, (255, 255, 255), "The End", position)

    def action(self):
        pass

    def update_hover(self, mouse_pos):
        pass


# Temporal tutorial text
class InitialInstructionText(TextGUI):
    def __init__(self, screen, position, time=10):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        text = """use LEFT and RIGHT to move and SPACE to jump...
        but be careful with the lights!"""
        TextGUI.__init__(self, screen, font, (255, 255, 255), text, position)
        self.time = time
        self.visible = False

    def action(self):
        pass

    def update_hover(self, mouse_pos):
        pass

    def draw(self, screen):
        if self.visible:
            super().draw(screen)

    def update(self, dt):
        self.time -= dt
        if self.time <= 0:
            self.visible = False
            self.time = 0
            
# Retry tutorial text
class RetryInstructionText(TextGUI):
    def __init__(self, screen, position, time=5):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        text = """lets try again, 
        this time be more careful"""
        TextGUI.__init__(self, screen, font, (255, 255, 255), text, position)
        self.time = time
        self.visible = True

    def action(self):
        pass

    def update_hover(self, mouse_pos):
        pass

    def draw(self, screen):
        if self.visible:
            super().draw(screen)

    def update(self, dt):
        self.time -= dt
        if self.time <= 0:
            self.visible = False
            self.time = 0
            
class CheckpointText(TextGUI):
    def __init__(self, screen, position):
        font = ResourceManager().load_font("Commodore-64-v621c.TTF", "assets/fonts", 20)
        TextGUI.__init__(
            self,
            screen,
            font,
            (255, 255, 255),
             """checkpoint reached! respawn set.""",
            position,
        )

    def action(self):
        pass