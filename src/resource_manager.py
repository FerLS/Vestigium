import pygame
from pygame.locals import RLEACCEL
import os 

class ResourceManager(object):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.images = {}

        return cls._instance

    def load_image(self, image_name, image_path, colorkey=None): 

        # Load image from disk if not already loaded 
        if image_name not in self.images:
            fullname = os.path.join(image_path, image_name)
            try:
                image = pygame.image.load(fullname)
            except pygame.error as message:
                print("Cannot load image:", image_name)
                raise SystemExit(message)
            image = image.convert_alpha()
            if colorkey is not None:    
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, RLEACCEL)
            self.images[image_name] = image

        return self.images[image_name]
    
"""    def obtain_subimage(file, x, y, width, height):
        image = """