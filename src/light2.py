import pygame
import math
from abc import abstractmethod


class Light(pygame.sprite.Sprite):
    def __init__(self, position, distance):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.distance = distance
        self.mask = None
        self.dirty = True  # Solo recalcular si hay cambios

        # Elementos requeridos por un Sprite
        size = int(distance * 2)
        self.image = pygame.Surface(
            (size, size), pygame.SRCALPHA
        )  # Imagen transparente
        self.rect = self.image.get_rect(
            center=self.position
        )  # Rect centrado en la posición
        self.rect.center = self.position

    def update(self, new_position=None, obstacles=None):
        if new_position and self.position != pygame.Vector2(new_position):
            self.position = pygame.Vector2(new_position)
            self.dirty = True
            self.rect.center = self.position  # <-- sincronizar rect con posición

        if self.dirty:
            self._generate_mask(obstacles or [])
            self.dirty = False

    def change_origin(self, new_position):
        self.position = pygame.Vector2(new_position)
        self.rect.center = self.position
        self.dirty = True

    @abstractmethod
    def _generate_mask(self, obstacles):
        pass

    def draw(self, screen, offset=(0, 0)):
        offset_x, offset_y = offset
        if self.mask:
            mask_surface = self.mask.to_surface(
                setcolor=((255, 209, 0, 150)), unsetcolor=(0, 0, 0, 0)
            )
            screen.blit(
                mask_surface,
                (
                    self.position.x - self.distance - offset_x,
                    self.position.y - self.distance - offset_y,
                ),
            )
        """debug_platform_rect = self.rect.move(-offset_x, -offset_y)
        pygame.draw.rect(screen, (0, 255, 0), debug_platform_rect, 1)"""


class CircularLight(Light):
    def __init__(self, position, radius, segments=170, ray_step=2, use_obstacles=True):
        super().__init__(position, radius)
        self.segments = segments
        self.ray_step = ray_step
        self.use_obstacles = use_obstacles  # Nuevo flag

    def _generate_mask(self, obstacles):
        size = int(self.distance * 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        center = pygame.Vector2(self.distance, self.distance)

        if not self.use_obstacles:
            # Luz circular completa sin casting
            pygame.draw.circle(surface, (255, 255, 255, 150), center, self.distance)
        else:
            # Luz con casting de rayos y colisiones
            points = [center]
            nearby_obstacles = [
                r
                for r in obstacles
                if self.position.distance_to(r.center) < self.distance + 50
            ]

            for i in range(self.segments):
                angle = math.radians(i * (360 / self.segments))
                direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                end_point = self._cast_ray(self.position, direction, nearby_obstacles)
                relative_point = (end_point - self.position) + center
                points.append(relative_point)

            pygame.draw.polygon(surface, (255, 255, 255, 150), points)

        self.mask = pygame.mask.from_surface(surface)

    def _cast_ray(self, origin, direction, obstacles):
        end = origin + direction * self.distance
        for i in range(0, int(self.distance), self.ray_step):
            point = origin + direction * i
            point_rect = pygame.Rect(point.x, point.y, 1, 1)
            for obstacle in obstacles:
                if obstacle.colliderect(point_rect):
                    return point
        return end

    def change_radius(self, new_radius):
        self.distance = new_radius
        self.rect.size = (new_radius * 2, new_radius * 2)
        self.rect.center = self.position
        self.dirty = True

    def get_radius(self):
        return self.distance


class ConeLight(Light):
    def __init__(self, position, direction, angle, distance, segments=60, ray_step=2):
        super().__init__(position, distance)
        self.direction = pygame.Vector2(direction).normalize()
        self.angle = math.radians(angle)
        self.segments = segments
        self.ray_step = ray_step

    def _generate_mask(self, obstacles):
        size = int(self.distance * 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        center = pygame.Vector2(self.distance, self.distance)
        start_angle = math.atan2(self.direction.y, self.direction.x) - self.angle / 2
        end_angle = start_angle + self.angle
        points = [center]

        nearby_obstacles = [
            r
            for r in obstacles
            if self.position.distance_to(r.center) < self.distance + 50
        ]

        for i in range(self.segments + 1):
            angle = start_angle + (end_angle - start_angle) * (i / self.segments)
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            end_point = self._cast_ray(self.position, direction, nearby_obstacles)
            relative_point = (end_point - self.position) + center
            points.append(relative_point)

        pygame.draw.polygon(surface, (255, 255, 0, 128), points)
        self.mask = pygame.mask.from_surface(surface)

    def _cast_ray(self, origin, direction, obstacles):
        end = origin + direction * self.distance
        for i in range(0, int(self.distance), self.ray_step):
            point = origin + direction * i
            point_rect = pygame.Rect(point.x, point.y, 1, 1)
            for obstacle in obstacles:
                if obstacle.colliderect(point_rect):
                    return point
        return end
