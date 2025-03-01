import pygame
import os
import random

from entities.light import Light
from resource_manager import ResourceManager
from utils.constants import MovementDirections, MovementType


class Gravedigger(pygame.sprite.Sprite):
    def __init__(self, x, y, tilemap):
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager = ResourceManager()
        self.walk_sheet = self.resource_manager.load_image(
            "enemy-walk.png", "assets\\enemy"
        )
        self.idle_sheet = self.resource_manager.load_image(
            "enemy-idle.png", "assets\\enemy"
        )

        self.tilemap = tilemap
        self.rect = pygame.Rect((0, 0), (42, 47))
        self.light = Light(
            x + 20, y, "assets/enemy/lantern.png"
        )  # Asociamos light ao farolillo
        self.image = self.idle_sheet.subsurface(self.rect)
        self.mask = pygame.mask.from_surface(self.image)

        self.initial_position = (x, y)  # posición inicial
        self.rect.x = x
        self.rect.y = y
        self.velocity = 1
        self.range = (200, 500)  # Range de movemento en x
        self.state = MovementType.IDLE
        self.movement = MovementDirections.LEFT
        self.time = random.randint(60, 120)  # Cada 60 ou 120 frames cambia de direccion

        self.walk_frames = self.load_frames(self.walk_sheet)
        self.idle_frames = self.load_frames(self.idle_sheet)
        self.imagePosture = 0
        self.animationSpeed = 5
        self.animationCounter = 0

        self.collided = False
        self.offset_x = 0

    # Cargar cada sheet
    def load_frames(self, sheet):
        frames = []
        frame_width = 42
        num_frames = sheet.get_width() // frame_width
        for i in range(num_frames):
            frame = sheet.subsurface((i * 42, 0, 42, 47))
            frames.append(frame)
        return frames

    # Animacion idle e walk
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

    # Moverse nun rango e aleatoriamente
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
                self.time = random.randint(60, 120)  # Novo tempo
        self.light.update_position(self)

    def collide(self, player):
        if self.mask.overlap(
            player.mask, (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        ):
            if (
                self.movement == MovementDirections.RIGHT
                and player.rect.x < self.rect.x
            ) or (
                self.movement == MovementDirections.LEFT and player.rect.x > self.rect.x
            ):
                player.get_key()
                self.stop()

    def stop(self):
        self.state = MovementType.IDLE
        self.collided = True

    # Cando estea preto comeza a andar
    def start(self, player):
        if not self.collided:
            distance = abs(self.rect.x - player.rect.x)
            if distance < 100:
                self.state = MovementType.WALK

    def check_collisions(self):
        colliders = self.tilemap.get_collision_rects()

        self.on_ground = False
        return

        # Colisiones en el eje Y
        self.rect.y += self.velocity
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity > 0:
                    self.rect.bottom = collider.top
                    self.velocity = 0
                    self.on_ground = True
                elif self.velocity < 0:
                    self.rect.top = collider.bottom
                    self.velocity = 0

        # Colisiones en el eje X
        self.rect.x += self.velocity
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity > 0:
                    self.rect.right = collider.left
                elif self.velocity < 0:
                    self.rect.left = collider.right

    def update(self, player, camera_scroll, screen):
        self.start(player)
        self.collide(player)
        self.move()
        self.animate()
        self.light.update_position(self)
        self.light.collide(player, self)
        self.check_collisions()
        self.draw(screen, camera_scroll)
        # self.rect.x = self.initial_position[0] - camera_scroll
        # print(f"Gravedigger position: ({self.rect.x}, {self.rect.y})")

    def draw(self, screen, camera_scroll):
        img = self.image

        if self.movement == MovementDirections.LEFT:
            img = pygame.transform.flip(img, 1, 0)

        self.offset_x += camera_scroll
        screen.blit(img, (self.rect.x - self.offset_x, self.rect.y))
        self.light.draw(screen)
