import pygame
import os
import random

from resource_manager import ResourceManager
from utils.constants import MovementDirections, MovementType, SCALE_FACTOR
from light2 import CircularLight  # Importa CircularLight


class Gravedigger(pygame.sprite.Sprite):
    def __init__(self, x, y, tilemap):
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager = ResourceManager()
        self.walk_sheet = self.scale_image(
            self.resource_manager.load_image("enemy-walk.png", "assets\\enemy")
        )
        self.idle_sheet = self.scale_image(
            self.resource_manager.load_image("enemy-idle.png", "assets\\enemy")
        )

        self.tilemap = tilemap
        self.rect = pygame.Rect((0, 0), (42 * SCALE_FACTOR, 47 * SCALE_FACTOR))

        self.image = self.idle_sheet.subsurface(self.rect)
        self.mask = pygame.mask.from_surface(self.image)

        self.initial_position = (x, y)
        self.rect.x = x
        self.rect.y = y
        self.velocity = 1
        self.range = (200, 500)
        self.state = MovementType.IDLE
        self.movement = MovementDirections.LEFT
        self.time = random.randint(60, 120)

        self.walk_frames = self.load_frames(self.walk_sheet)
        self.idle_frames = self.load_frames(self.idle_sheet)
        self.imagePosture = 0
        self.animationSpeed = 5
        self.animationCounter = 0

        self.collided = False
        self.offset_x = 0

        # Crear una luz circular
        self.light = CircularLight(
            (self.rect.centerx - 20, self.rect.centery), radius=15
        )

    def scale_image(self, image):
        width, height = image.get_width(), image.get_height()
        return pygame.transform.scale(
            image, (width * SCALE_FACTOR, height * SCALE_FACTOR)
        )

    def load_frames(self, sheet):
        frames = []
        frame_width = 42 * SCALE_FACTOR
        frame_height = 47 * SCALE_FACTOR
        num_frames = sheet.get_width() // frame_width
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def animate(self):
        self.animationCounter += 1
        if self.animationCounter >= self.animationSpeed:
            self.animationCounter = 0
            self.imagePosture = (self.imagePosture + 1) % len(
                self.walk_frames
                if self.state == MovementType.WALK
                else self.idle_frames
            )
        if self.state == MovementType.WALK:
            self.image = self.walk_frames[self.imagePosture]
        else:
            self.image = self.idle_frames[self.imagePosture]

    def move(self):
        if self.state == MovementType.WALK:
            if self.movement == MovementDirections.LEFT:
                self.rect.x -= self.velocity
            else:
                self.rect.x += self.velocity

            if self.rect.x <= self.initial_position[0] + self.range[0]:
                self.movement = MovementDirections.RIGHT
            elif self.rect.x >= self.initial_position[0] + self.range[1]:
                self.movement = MovementDirections.LEFT

            self.time -= 1
            if self.time <= 0:
                self.movement = random.choice(
                    [MovementDirections.LEFT, MovementDirections.RIGHT]
                )
                self.time = random.randint(60, 120)

    def collide(self, player):
        if self.mask.overlap(
            player.mask, (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        ) and not player.is_dying and not player.dead:
            player.dying()

    def stop(self):
        self.state = MovementType.IDLE
        self.collided = True

    def start(self, player):
        if not self.collided:
            distance = abs(self.rect.x - player.rect.x)
            if distance < 300:
                self.state = MovementType.WALK

    def update(self, player):
        self.start(player)
        self.collide(player)
        self.move()
        self.animate()

        # Actualizar la posición de la luz
        light_offset = -25 if self.movement == MovementDirections.LEFT else 25
        self.light.update(
            new_position=(self.rect.centerx + light_offset, self.rect.centery + 15)
        )

    def draw(self, screen, camera_scroll):
        img = self.image

        if self.movement == MovementDirections.LEFT:
            img = pygame.transform.flip(img, 1, 0)

        offset_x, offset_y = camera_scroll
        screen.blit(img, (self.rect.x - offset_x, self.rect.y - offset_y))

        # Dibujar la luz
        self.light.draw(screen, offset=camera_scroll)
