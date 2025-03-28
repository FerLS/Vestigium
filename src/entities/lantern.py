import pygame
from resource_manager import ResourceManager
import math

from utils.constants import SCALE_FACTOR


class Lantern(pygame.sprite.Sprite):
    def __init__(self, position, path, scale=4, speed=2):
        super().__init__()
        self.speed = speed
        self.radius = 190 * SCALE_FACTOR  # Radio del collider circular
        self.angle = 0  # Ángulo de inclinación
        self.float_offset = 0  # Desplazamiento vertical para la flotación
        self.float_speed = 0.1  # Velocidad de la oscilación
        self.float_amplitude = 20  # Amplitud de la oscilación
        self.time = 0  # Contador de tiempo para la flotación

        # Cargar imagen de la linterna
        original_image = ResourceManager().load_image("Lantern.png", "assets/images")
        width, height = original_image.get_size()
        self.original_image = pygame.transform.scale(
            original_image, (width * scale, height * scale)
        )
        self.image = self.original_image.copy()

        # Cargar imagen de la luz
        light_image = ResourceManager().load_image("Light.png", "assets/images")
        light_width, light_height = light_image.get_size()
        self.light_image = pygame.transform.scale(
            light_image, (light_width * scale, light_height * scale)
        )

        # Ajustar rectángulo usando el centro
        self.rect = self.image.get_rect(center=position)
        self.pos = pygame.math.Vector2(position)  # Posición absoluta en el mundo

        # Convertir path a posiciones absolutas en el mundo
        self.path = [pygame.math.Vector2(p) for p in path]

        # Iniciar en el primer punto correctamente
        self.current_point_index = 0
        self.target = self.path[self.current_point_index]

    def update(self, player, tilemap, offset=(0, 0)):
        """Actualiza la posición de la linterna y gestiona colisiones."""
        # Ajustar el target teniendo en cuenta el offset
        target_position = self.target  # Ya es una coordenada absoluta

        # Calcular vector y distancia hacia el destino
        vector_to_target = target_position - self.pos
        distance = vector_to_target.length()

        if (
            distance <= self.speed
        ):  # Si llega exactamente al punto, avanzar al siguiente
            self.pos = target_position
            self.current_point_index = (self.current_point_index + 1) % len(self.path)
            self.target = self.path[self.current_point_index]  # Nuevo destino
        elif distance > 0:  # Asegurarse de que el vector no sea nulo
            direction = vector_to_target.normalize()
            self.pos += direction * min(
                self.speed, distance
            )  # Movimiento constante y preciso

            # Suavizar la rotación en el eje X
            target_angle = (
                direction.x * -10
            )  # Inclinación basada en movimiento horizontal
            self.angle += (
                target_angle - self.angle
            ) * 0.1  # Interpolación para suavidad

        # Aplicar efecto de flotación
        self.time += self.float_speed
        self.float_offset = math.sin(self.time) * self.float_amplitude

        # Rotar la imagen
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Actualizar la posición del rectángulo (coordenadas de pantalla)
        self.rect.center = (
            round(self.pos.x - offset[0]),
            round(self.pos.y - offset[1] + self.float_offset),
        )

        # Colisión con el jugador usando el collider circular
        distance_to_player = self.pos.distance_to((player.rect.x, player.rect.y))
        if distance_to_player <= self.radius and not player.is_dying and not player.dead:
            safe_tiles = tilemap.get_safe_rects()
            player_in_safe_zone = any(
                player.rect.colliderect(safe_tile) for safe_tile in safe_tiles
            )
            if not player_in_safe_zone:
                player.dying()

    def draw(self, screen, offset=(0, 0)):
        """Dibuja la linterna, su luz y el collider circular en la pantalla con desplazamiento de cámara."""
        # Calcular la posición de la luz con el offset de la cámara
        light_pos = (
            self.pos.x - self.light_image.get_width() // 2 - offset[0],
            self.pos.y
            - self.light_image.get_height() // 2
            - offset[1]
            + self.float_offset,
        )

        # Dibujar la luz con opacidad ajustada
        light_surface = self.light_image.copy()
        light_surface.set_alpha(128)
        screen.blit(light_surface, light_pos)

        # Dibujar la linterna encima, aplicando el offset
        screen.blit(self.image, (self.rect.x, self.rect.y))
