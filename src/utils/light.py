import pygame
import math
from abc import abstractmethod
from typing import Optional, Sequence



class Light(pygame.sprite.Sprite):
    """
    Base class for dynamic light sources. Handles position, range, and rendering.
    Intended to be subclassed with specific light behaviors.
    """

    def __init__(self, position: tuple[float, float], distance: float, use_obstacles: bool = True):
        self.position: pygame.Vector2 = pygame.Vector2(position)
        self.distance: float = distance
        self.mask: Optional[pygame.mask.Mask] = None
        self.use_obstacles: bool = use_obstacles
        self.intensity: float = 1.0

        super().__init__()

        size = int(distance * 2)
        self.image: pygame.Surface = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect(center=self.position)
        self.rect.center = self.position

    def update(
        self,
        new_position: Optional[tuple[float, float]] = None,
        obstacles: Optional[Sequence[pygame.Rect]] = None,
        camera_rect: Optional[pygame.Rect] = None
    ):
        """
        Updates the light mask and position. Only regenerates the mask if visible.
        """
        if new_position and self.position != pygame.Vector2(new_position):
            self.position = pygame.Vector2(new_position)
            self.rect.center = self.position

        if self.mask is None:
            self._generate_mask(obstacles or [])

        light_area = pygame.Rect(0, 0, 300, 300)
        light_area.center = self.position

        if not camera_rect or light_area.colliderect(camera_rect):
            self._generate_mask(obstacles or [])

    @abstractmethod
    def _generate_mask(self, obstacles: Sequence[pygame.Rect]):
        """
        Abstract method to generate the light mask. Must be implemented by subclasses.
        """
        pass

    def draw(self, screen: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        """
        Draws the light's mask to the screen using an alpha blend.
        """
        offset_x, offset_y = offset
        if self.mask:
            mask_surface = self.mask.to_surface(
                setcolor=(255, 209, 0, int(150 * self.intensity)),
                unsetcolor=(0, 0, 0, 0)
            )
            screen.blit(
                mask_surface,
                (self.position.x - self.distance - offset_x, self.position.y - self.distance - offset_y)
            )



class CircularLight(Light):
    """
    Light source that casts a circular field of light.
    Optionally raycasts around obstacles to simulate realistic lighting.
    """

    def __init__(
        self,
        position: tuple[float, float],
        radius: float,
        segments: int = 170,
        ray_step: int = 2,
        use_obstacles: bool = True
    ):
        super().__init__(position, radius, use_obstacles)
        self.segments = segments
        self.ray_step = ray_step

    def _generate_mask(self, obstacles: Sequence[pygame.Rect]):
        """
        Generates a circular light mask with or without raycasting around obstacles.
        """
        size = int(self.distance * 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        center = pygame.Vector2(self.distance, self.distance)

        if not self.use_obstacles:
            pygame.draw.circle(surface, (255, 255, 255, 150), center, self.distance)
        else:
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

    def _cast_ray(
        self,
        origin: pygame.Vector2,
        direction: pygame.Vector2,
        obstacles: Sequence[pygame.Rect]
    ) -> pygame.Vector2:
        """
        Casts a ray in a direction until it hits an obstacle or reaches max distance.
        """
        end = origin + direction * self.distance
        for i in range(0, int(self.distance), self.ray_step):
            point = origin + direction * i
            point_rect = pygame.Rect(point.x, point.y, 1, 1)
            for obstacle in obstacles:
                if obstacle.colliderect(point_rect):
                    return point
        return end

    def change_radius(self, new_radius: float):
        """
        Dynamically changes the radius of the light.
        """
        self.distance = new_radius
        self.rect.size = (new_radius * 2, new_radius * 2)
        self.rect.center = self.position
        self.dirty = True

    def get_radius(self) -> float:
        """
        Returns the current radius of the light.
        """
        return self.distance


class ConeLight(Light):
    """
    Light source that casts a cone-shaped beam (useful for flashlights, vision cones).
    """

    def __init__(
        self,
        position: tuple[float, float],
        direction: tuple[float, float],
        angle: float,
        distance: float,
        segments: int = 60,
        ray_step: int = 2,
        use_obstacles: bool = True
    ):
        super().__init__(position, distance, use_obstacles)
        self.direction = pygame.Vector2(direction).normalize()
        self.angle = math.radians(angle)
        self.segments = segments
        self.ray_step = ray_step

    def _generate_mask(self, obstacles: Sequence[pygame.Rect]):
        """
        Generates a cone-shaped light mask using raycasting and angle spread.
        """
        size = int(self.distance * 2)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        center = pygame.Vector2(self.distance, self.distance)
        start_angle = math.atan2(self.direction.y, self.direction.x) - self.angle / 2
        end_angle = start_angle + self.angle
        points = [center]

        if not self.use_obstacles:
            for i in range(self.segments + 1):
                angle = start_angle + (end_angle - start_angle) * (i / self.segments)
                direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                end_point = self.position + direction * self.distance
                relative_point = (end_point - self.position) + center
                points.append(relative_point)
        else:
            nearby_obstacles = [r for r in obstacles if self.position.distance_to(r.center) < self.distance + 50]
            for i in range(self.segments + 1):
                angle = start_angle + (end_angle - start_angle) * (i / self.segments)
                direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                end_point = self._cast_ray(self.position, direction, nearby_obstacles)
                relative_point = (end_point - self.position) + center
                points.append(relative_point)

        pygame.draw.polygon(surface, (255, 255, 0, 128), points)
        pygame.draw.polygon(surface, (255, 255, 0, 128), points)
        self.mask = pygame.mask.from_surface(surface)

    def _cast_ray(
        self,
        origin: pygame.Vector2,
        direction: pygame.Vector2,
        obstacles: Sequence[pygame.Rect]
    ) -> pygame.Vector2:
        """
        Casts a ray in a direction and stops when hitting an obstacle.
        """
        end = origin + direction * self.distance
        for i in range(0, int(self.distance), self.ray_step):
            point = origin + direction * i
            point_rect = pygame.Rect(point.x, point.y, 1, 1)
            for obstacle in obstacles:
                if obstacle.colliderect(point_rect):
                    return point
        return end
