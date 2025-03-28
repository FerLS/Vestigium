import pygame
from director import Director
from scenes.startMenu import StartMenu

if __name__ == "__main__":

    pygame.init()
    director = Director()
    first_scene = StartMenu(director)
    director.stack_scene(first_scene)
    director.run()
    pygame.quit()    
    