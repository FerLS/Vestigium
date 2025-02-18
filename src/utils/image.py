import pygame
from pygame.locals import RLEACCEL
import os

def load_image(name: str, colorkey=None):
    fullname = os.path.join("assets\images\\", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:    
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image