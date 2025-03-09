import pygame
import math
from abc import ABC, abstractmethod

class Light(ABC):
    def __init__(self, position, distance):
        self.position = pygame.Vector2(position)
        self.distance = distance
        self.mask = None
        self.dirty = True  # Solo recalcular si hay cambios

    def update(self, new_position=None, obstacles=None):
        if new_position and self.position != pygame.Vector2(new_position):
            self.position = pygame.Vector2(new_position)
            self.dirty = True

        if self.dirty:
            self._generate_mask(obstacles or [])
            self.dirty = False

    @abstractmethod
    def _generate_mask(self, obstacles):
        pass

    def draw(self, screen):
        if self.mask:
            mask_surface = self.mask.to_surface(setcolor=(255, 255, 255, 100), unsetcolor=(0, 0, 0, 0))
            screen.blit(mask_surface, (self.position.x - self.distance, self.position.y - self.distance))


class CircularLight(Light):
    def __init__(self, position, radius, segments=60, ray_step=2):
        super().__init__(position, radius)
        self.segments = segments
        self.ray_step = ray_step

    def _generate_mask(self, obstacles):
        size = int(self.distance * 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        center = pygame.Vector2(self.distance, self.distance)
        points = [center]

        nearby_obstacles = [r for r in obstacles if self.position.distance_to(r.center) < self.distance + 50]

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

        nearby_obstacles = [r for r in obstacles if self.position.distance_to(r.center) < self.distance + 50]

        for i in range(self.segments + 1):
            angle = start_angle + (end_angle - start_angle) * (i / self.segments)
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
