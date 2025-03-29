import pygame
from pygame.locals import RLEACCEL
import os


class ResourceManager:
    """
    Singleton class responsible for loading and caching images, fonts, and sounds.
    Prevents redundant resource loading by keeping them in memory.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.images =  {}
            cls.fonts = {}
            cls.sounds = {}
        return cls._instance

    def load_image(self, 
                   image_name: str, 
                   image_path: str, 
                   colorkey=None) -> pygame.Surface:
        """
        Loads an image from disk and caches it. Applies optional transparency.

        :param image_name: Name of the image file (e.g., "image.png").
        :param image_path: Path to the directory containing the image.
        :param colorkey: Color key for transparency (default is None). If -1, uses the top-left pixel color.
        :return: A pygame.Surface object representing the loaded image.
        """
        if image_name not in self.images:
            fullname = os.path.join(image_path, image_name)
            try:
                image = pygame.image.load(fullname)
            except pygame.error as message:
                print("Cannot load image:", image_name)
                raise SystemExit(message)
            image = image.convert_alpha()
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
            self.images[image_name] = image

        return self.images[image_name]

    def load_font(self, 
                  font_name: str, 
                  font_path: str, 
                  size: int) -> pygame.font.Font:
        """
        Loads a font from disk and caches it.

        :param font_name: Name of the font file (e.g., "font.ttf").
        :param font_path: Path to the directory containing the font.
        :param size: Size of the font in points.
        :return: A pygame.font.Font object representing the loaded font.
        """
        if font_name not in self.fonts:
            fullname = os.path.join(font_path, font_name)
            try:
                font = pygame.font.Font(fullname, size)
            except pygame.error as message:
                print("Cannot load font:", font_name)
                raise SystemExit(message)
            self.fonts[font_name] = font

        return self.fonts[font_name]

    def load_sound(self, 
                   sound_name: str, 
                   sound_path: str) -> pygame.mixer.Sound:
        """
        Loads a sound from disk and caches it.

        :param sound_name: Name of the sound file (e.g., "sound.wav").
        :param sound_path: Path to the directory containing the sound.
        :return: A pygame.mixer.Sound object representing the loaded sound.
        """
        if sound_name not in self.sounds:
            fullname = os.path.join(sound_path, sound_name)
            try:
                sound = pygame.mixer.Sound(fullname)
            except pygame.error as message:
                print("Cannot load sound:", sound_name)
                raise SystemExit(message)
            self.sounds[sound_name] = sound

        return self.sounds[sound_name]
