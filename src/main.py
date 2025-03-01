import pygame
from director import Director
from scenes.cemeteryPhase import CemeteryPhase

if __name__ == "__main__":
    pygame.init()
    director = Director()
    first_scene = CemeteryPhase(director, director.screen) #Esta no debería ser la primera escena, la primera debería ser un Menu
    #TODO first_scene = MenuScene(director)
    director.stack_scene(first_scene)
    director.run()
    pygame.quit()