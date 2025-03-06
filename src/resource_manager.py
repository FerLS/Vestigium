import pygame
from pygame.locals import RLEACCEL
import os 

class ResourceManager(object):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.images = {}
            cls.fonts = {}
            cls.sounds = {}            

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
    
    def load_font(self, font_name, font_path, size):
        
        # Load font from disk if not already loaded
        if font_name not in self.fonts:
            fullname = os.path.join(font_path, font_name)
            try:
                font = pygame.font.Font(fullname, size)
            except pygame.error as message:
                print("Cannot load font:", font_name)
                raise SystemExit(message)
            self.fonts[font_name] = font

        return self.fonts[font_name]
    
    def load_sound(self, sound_name, sound_path):
        
        # Load font from disk if not already loaded
        if sound_name not in self.sounds:
            fullname = os.path.join(sound_path, sound_name)
            try:
                sound = pygame.mixer.Sound(fullname)
            except pygame.error as message:
                print("Cannot load sound:", sound_name)
                raise SystemExit(message)
            self.sounds[sound_name] = sound

        return self.sounds[sound_name]
