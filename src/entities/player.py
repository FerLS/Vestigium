import pygame
from utils.images import extract_frames
import os

from utils.constants import (
    CAMERA_LIMITS_Y,
    MAX_FALL_SPEED,
    MOVE_SPEED,
    SCALE_FACTOR,
    MovementDirections,
    MovementType,
)
from resource_manager import ResourceManager
from sound_manager import SoundManager

INITIAL_FALL_SPEED = 5

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tilemap):
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager = ResourceManager()
        self.sound_manager = SoundManager()
        self.sheet = self.resource_manager.load_image("player_spritesheet.png", "assets\\images")

        # Animations
        self.animations = {
            "idle": extract_frames(self.sheet, 0, 0, 32, 32, 2, SCALE_FACTOR) + extract_frames(self.sheet, 0, 32, 32, 32, 2, SCALE_FACTOR),
            "walk": extract_frames(self.sheet, 0, 96, 32, 32, 8, SCALE_FACTOR),
            "jump": extract_frames(self.sheet, 0, 160, 32, 32, 8, SCALE_FACTOR),
            "fall": extract_frames(self.sheet, 128, 160, 32, 32, 1, SCALE_FACTOR),
            "dead": extract_frames(self.sheet, 0, 192, 32, 32, 3, SCALE_FACTOR),
        }

        # Initial state
        self.current_animation = self.animations["idle"]
        self.frame_index = 0
        self.image = self.current_animation[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.fliped = False
        self.animation_speed = 0.25
        self.animation_timer = 0
        self.mask = pygame.mask.from_surface(self.image)

        # Collisions
        self.tilemap = tilemap
        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.on_ceil = False

        # Physics
        self.dead = False
        self.gravity = 0.5
        self.velocity_x = 0
        self.velocity_y = 0
        self.movement = MovementType.IDLE
        self.jump_power = -10
        
        self.step_sound_number = 0

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_animation)
            
            new_frame = self.current_animation[self.frame_index]
            old_center = self.rect.center  

            self.image = new_frame
            if self.fliped:
                self.image = pygame.transform.flip(self.image, True, False)

            self.rect = self.image.convert_alpha().get_rect()
            
            self.rect.center = old_center
        

    def move(self, direction: MovementDirections, camera_scroll_x):
        if direction == MovementDirections.LEFT and not self.on_wall_left:
            self.velocity_x = (-MOVE_SPEED - camera_scroll_x) * SCALE_FACTOR
            self.fliped = True
            self.current_animation = self.animations["walk"]

        elif direction == MovementDirections.RIGHT and not self.on_wall_right:
            self.velocity_x = (MOVE_SPEED - camera_scroll_x) * SCALE_FACTOR
            self.fliped = False
            self.current_animation = self.animations["walk"]

        else:
            if self.on_ground:
                self.velocity_x = 0
                self.current_animation = self.animations["idle"]

    def jump(self):
        if self.on_ground:
            self.on_ground = False
            self.current_animation = self.animations["jump"]
            self.velocity_y = self.jump_power * SCALE_FACTOR

    def apply_gravity(self):

        if not self.on_ground:
            self.velocity_y += self.gravity * SCALE_FACTOR
            if self.velocity_y >= MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED
        else: 
            self.current_animation = self.animations["idle"]

        if self.rect.bottom > CAMERA_LIMITS_Y[1]:
            self.velocity_y = 0

    def check_collisions(self, camera_scroll_x, camera_scroll_y):
        colliders = self.tilemap.get_collision_rects()

        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.on_ceil = False

        # Colisiones en el eje Y
        if camera_scroll_y >= 0:
            self.rect.y += self.velocity_y
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity_y > 0 or camera_scroll_y > 0:
                    self.rect.bottom = collider.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0 or camera_scroll_y < 0:
                    self.rect.top = collider.bottom
                    self.velocity_y = 0
                    self.on_ceil = True

        # Colisiones en el eje X

        self.rect.x += self.velocity_x
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity_x > 0 or camera_scroll_x > 0:
                    self.rect.right = collider.left
                    self.on_wall_right = True
                    self.velocity_x = 0
                elif self.velocity_x < 0 or camera_scroll_x < 0:
                    self.rect.left = collider.right
                    self.on_wall_left = True
                    self.velocity_x = 0

    def get_key(self):
        print("You won")

    def die(self):
        self.dead = True
        self.current_animation = self.animations["dead"]
        self.frame_index = 0
        print("You died")

    def update(self, keys, camera_scroll_x, camera_scroll_y, dt):
        if not self.dead:
            if keys[pygame.K_LEFT]:
                if self.on_ground:
                    sound_name = "snow_step_" + str(self.step_sound_number) + ".ogg"
                    self.sound_manager.play_sound(sound_name, "assets\\sounds")
                    self.step_sound_number = (self.step_sound_number + 1) % 2

                self.move(MovementDirections.LEFT, camera_scroll_x)
            elif keys[pygame.K_RIGHT]:
                if self.on_ground:
                    sound_name = "snow_step_" + str(self.step_sound_number) + ".ogg"
                    self.sound_manager.play_sound(sound_name, "assets\\sounds")
                    self.step_sound_number = (self.step_sound_number + 1) % 2
                self.move(MovementDirections.RIGHT, camera_scroll_x)
            else:
                self.move(None, camera_scroll_x)

            if keys[pygame.K_SPACE]:
                self.jump()

            if self.velocity_y < 0:
                self.current_animation = self.animations["fall"]

            self.check_collisions(camera_scroll_x, camera_scroll_y)
            self.apply_gravity()
            self.update_animation(dt)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
