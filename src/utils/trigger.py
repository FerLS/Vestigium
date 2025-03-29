import pygame

class Trigger:
    def __init__(self, rect: pygame.Rect, action: callable, triggered_once: bool=True, display_time: int=3):
        """
        Class to create a trigger in the game. A trigger is an area in the game that when the player
        collides with it, it triggers an action. 

        param rect: The area of the trigger.
        param action: The action to execute when the player collides with the trigger.
        param triggered_once:
            If True, the trigger will only be executed once.
            If False, the trigger will be executed every time the player collides with it.
        param display_time: The time in seconds to display the text.
        """
        self.rect = rect  
        self.action = action 
        self.triggered_once = triggered_once
        self.triggered = False

        self.text = None
        self.display_time = display_time
        self.current_time = 0

    def check(self, player_rect: pygame.Rect):
        """
        Check if the player is colliding with the trigger and execute the action.

        param player_rect: The rect of the player.
        """
        if self.rect.colliderect(player_rect) and (not self.triggered or not self.triggered_once):
            self.text = self.action()
            self.triggered = True
            self.current_time = self.display_time

    def update(self, dt: float):
        """
        Update the trigger text (either to display it or to remove it).

        param dt: The time in seconds since the last update.
        """
        if self.text is not None and self.current_time > 0:
            self.current_time -= dt
            if self.current_time <= 0:
                self.text = None

    def draw(self, screen: pygame.Surface):
        """
        Draw the trigger text.

        param screen: The screen to draw the text.
        """
        if self.text is not None:
            self.text.draw(screen)