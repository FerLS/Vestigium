import math
import pygame
import random
from light2 import CircularLight

class Firefly(pygame.sprite.Sprite):
    def __init__(self, x, y, movement_bounds=None, movement_type="random"):
        super().__init__()
        self.RADIUS = 5
        self.radius_variation = 2
        self.blink_interval = 15
        self.current_radius = self.RADIUS

        self.light = CircularLight((x, y), self.RADIUS + 20, use_obstacles=False)
        self.rect = pygame.Rect(x, y, self.RADIUS * 2, self.RADIUS * 2)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.max_speed = 1.5
        self.acceleration_change = 0.2
        self.movement_bounds = movement_bounds
        self.movement_type = movement_type
        
        self.start_x = x
        self.start_y = y

        self.blink_timer = 0
        self.blink_up = True

        self.time = 0
        self.speed = random.uniform(8, 10) if y > 500 else random.uniform(2, 4)
        self.wave_amplitude = random.uniform(1, 4) if y > 250 else 6
        self.wave_frequency = random.uniform(0.01, 0.1)
        
        self.vertical_direction = random.choice([1, -1])
        self.horizontal_direction = random.choice([1, -1])
        
    def update(self):
        
        if self.movement_type == "random":
            # Movimiento oscilante
            delta = pygame.math.Vector2(
                random.uniform(-self.acceleration_change, self.acceleration_change),
                random.uniform(-self.acceleration_change, self.acceleration_change)
            )
            self.velocity += delta

            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y
      
            if self.movement_bounds:
                if not self.movement_bounds.contains(self.rect):
                    if self.rect.left < self.movement_bounds.left or self.rect.right > self.movement_bounds.right:
                        self.velocity.x *= -1
                    if self.rect.top < self.movement_bounds.top or self.rect.bottom > self.movement_bounds.bottom:
                        self.velocity.y *= -1
                    self.rect.clamp_ip(self.movement_bounds)
                          
        elif self.movement_type == "wave":
            self._move()
            
        elif self.movement_type == "vertical":
            self.rect.y += 1 * self.vertical_direction
            if abs(self.rect.y - self.start_y) >= 100:
                self.vertical_direction *= -1
            self.time += 1

        elif self.movement_type == "horizontal":
            self.rect.x += 1 * self.horizontal_direction
            if abs(self.rect.x - self.start_x) >= 100:
                self.horizontal_direction *= -1
            self.time += 1

              
        # Parpadeo
        self.blink_timer += 1
        if self.blink_timer >= self.blink_interval:
            self.blink_up = not self.blink_up
            self.blink_timer = 0

        self.current_radius = self.RADIUS + self.radius_variation if self.blink_up else self.RADIUS

        self.light.update(new_position=self.rect.center)
        self.light.change_radius(self.current_radius + 20)
        
    def _move(self):
        if self.velocity == pygame.math.Vector2(0, 0):
            return

        self.time += 1
        wave_offset = self.wave_amplitude * math.sin(self.time * self.wave_frequency)

        if self.start_x < 500:
            self.rect.x += self.speed
        elif self.start_x > 500:
            self.rect.x -= self.speed

        self.rect.y += wave_offset
        
        if self.rect.left > 1000 or self.rect.right < 0:
            self.reset()
    
    def reset(self, reason="touched_bounds", delay=False):
            
        if reason == "touched_bounds":
            self.rect.x = random.choice([0, 1000])
            if self.start_y <= 250:
                self.rect.y = random.randint(100, 250)
            else:
                self.rect.y = random.randint(250, 700)
                
        elif reason == "life_decreased" and not delay:
            self.rect.x = self.start_x
            self.rect.y = self.start_y
            
        self.speed = random.uniform(8, 10) if self.rect.y > 500 else random.uniform(2, 4)
        self.wave_amplitude = random.uniform(1, 4) if self.rect.y > 250 else 6
        self.wave_frequency = random.uniform(0.01, 0.1)
        
        if not delay:
            self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            self.time = 0
            self.light.update(new_position=self.rect.center)

    def stop(self):
        self.velocity = pygame.math.Vector2(0, 0)
        self.light.update(new_position=self.rect.center)

    def draw(self, screen, offset=(0, 0)):
        offset_x, offset_y = offset
        image = pygame.Surface((self.current_radius * 3, self.current_radius * 3), pygame.SRCALPHA)
        pygame.draw.circle(image, (255, 255, 100), (self.current_radius, self.current_radius), self.current_radius)
        draw_pos = self.rect.centerx - self.current_radius - offset_x, self.rect.centery - self.current_radius - offset_y
        screen.blit(image, draw_pos)
        self.light.draw(screen, offset)
