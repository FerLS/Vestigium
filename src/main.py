import pygame
from director import Director
from scenes.menus.start_menu import StartMenu

if __name__ == "__main__":
    """
    Entry point of the game. Initializes Pygame, sets up the director and
    the initial scene, and starts the game loop.
    """
    pygame.init()
    director = Director()
    first_scene = StartMenu(director)
    director.stack_scene(first_scene)
    director.run()
    pygame.quit()
