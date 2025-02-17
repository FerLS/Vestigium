import pygame


class Suelo(pygame.sprite.Sprite):
    def __init__(self, posicion, ancho, altura):
        super().__init__()
        self.image = pygame.Surface((ancho, altura))
        self.image.fill((100, 100, 100))  # Color gris
        self.rect = self.image.get_rect(topleft=posicion)
        self.mask = pygame.mask.from_surface(self.image)  # Para colisiones precisas
