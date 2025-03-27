import pygame
from resource_manager import ResourceManager


class Lantern(pygame.sprite.Sprite):
    def __init__(self, position, path, scale=4, speed=2):
        super().__init__()
        self.speed = speed

        # Cargar imagen de la linterna
        original_image = ResourceManager().load_image("Lantern.png", "assets/images")
        width, height = original_image.get_size()
        self.image = pygame.transform.scale(
            original_image, (width * scale, height * scale)
        )

        # Cargar imagen de la luz
        light_image = ResourceManager().load_image("Light.png", "assets/images")
        light_width, light_height = light_image.get_size()
        self.light_image = pygame.transform.scale(
            light_image, (light_width * scale, light_height * scale)
        )

        # Generar máscara de colisión para la luz (ignora transparencia)
        self.mask = pygame.mask.from_surface(self.light_image)

        # Ajustar rectángulo usando el centro
        self.rect = self.image.get_rect(center=position)
        self.pos = pygame.math.Vector2(position)  # Posición absoluta en el mundo

        # Convertir path a posiciones absolutas en el mundo

        self.path = [pygame.math.Vector2(p) for p in path]
        # Ordenar los puntos del path

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
        else:
            direction = vector_to_target.normalize()
            self.pos += direction * self.speed  # Movimiento constante

        # Actualizar la posición del rectángulo (coordenadas de pantalla)
        self.rect.center = (
            round(self.pos.x - offset[0]),
            round(self.pos.y - offset[1]),
        )

        # Ajustar la posición de la máscara (coincide con la luz)
        light_rect = self.light_image.get_rect(center=self.rect.center)

        # Colisión con el jugador solo en píxeles visibles de la luz
        if player.mask.overlap(
            self.mask, (light_rect.x - player.rect.x, light_rect.y - player.rect.y)
        ):
            safe_tiles = tilemap.get_safe_rects()
            player_in_safe_zone = any(
                player.rect.colliderect(safe_tile) for safe_tile in safe_tiles
            )
            if not player_in_safe_zone:
                player.is_dying = True

    def draw(self, screen, offset=(0, 0)):
        """Dibuja la linterna y su luz en la pantalla con desplazamiento de cámara."""
        # Calcular la posición de la luz con el offset de la cámara
        light_pos = (
            self.pos.x - self.light_image.get_width() // 2 - offset[0],
            self.pos.y - self.light_image.get_height() // 2 - offset[1],
        )

        # Dibujar la linterna encima, aplicando el offset
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Dibujar la luz con opacidad ajustada
        light_surface = self.light_image.copy()
        light_surface.set_alpha(128)
        screen.blit(light_surface, light_pos)
