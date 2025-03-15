# player.py
from time import sleep
import pygame
from utils.images import extract_frames
from utils.constants import (
    MAX_FALL_SPEED,
    MOVE_SPEED,
    SCALE_FACTOR,
    MovementType,
    CAMERA_LIMITS_Y,
)
from resource_manager import ResourceManager


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tilemap, obstacles):
        super().__init__()

        # Load resources
        self.resource_manager = ResourceManager()
        sheet = self.resource_manager.load_image("player_spritesheet.png", "assets\\images")

        # Animations
        self.animations = {
            "idle": extract_frames(sheet, 0, 0, 32, 32, 2, SCALE_FACTOR)
            + extract_frames(sheet, 0, 32, 32, 32, 2, SCALE_FACTOR),
            "walk": extract_frames(sheet, 0, 96, 32, 32, 8, SCALE_FACTOR),
            "jump": extract_frames(sheet, 0, 160, 32, 32, 8, SCALE_FACTOR),
            "fall": extract_frames(sheet, 128, 160, 32, 32, 1, SCALE_FACTOR),
            "dead": extract_frames(sheet, 0, 192, 32, 32, 6, SCALE_FACTOR),
        }

        self.current_animation = self.animations["idle"]
        self.frame_index = 0
        self.animation_speed = 0.25
        self.animation_timer = 0

        self.image = self.current_animation[self.frame_index]

        self.rect = pygame.Rect(0, 0, 16 * SCALE_FACTOR, 32 * SCALE_FACTOR)


        # Movement & Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.jump_power = -10 * SCALE_FACTOR
        self.gravity = 0.5 * SCALE_FACTOR
        self.flipped = False
        self.on_ground = False

        self.tilemap = tilemap
        self.obstacles = obstacles
        self.is_dying = False
        self.dead = False

    # Movement API
    def move_left(self):
        self.velocity_x = -MOVE_SPEED * SCALE_FACTOR
        self.flipped = True
        if self.on_ground:
            self.set_animation("walk")

    def move_right(self):
        self.velocity_x = MOVE_SPEED * SCALE_FACTOR
        self.flipped = False
        if self.on_ground:
            self.set_animation("walk")

    def stop(self):
        self.velocity_x = 0
        if self.on_ground:
            self.set_animation("idle")

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
            self.set_animation("jump")

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += self.gravity
            if self.velocity_y > 0:
                self.set_animation("fall")
            if self.velocity_y > MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_animation)
            if self.is_dying and self.frame_index == 5:
                self.dead = True

        new_frame = self.current_animation[self.frame_index]
        self.image = pygame.transform.flip(new_frame, True, False) if self.flipped else new_frame
        self.mask = pygame.mask.from_surface(self.image)


    def set_animation(self, name):
        if self.current_animation != self.animations[name]:
            self.current_animation = self.animations[name]
            self.frame_index = 0
            self.animation_timer = 0

    def check_collisions(self):
        self.on_ground = False
        colliders = self.tilemap.get_collision_rects()
        self.bouncy_obstacles = self.obstacles
        colliders += self.obstacles

        # Vertical
        self.rect.y += self.velocity_y
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity_y > 0:
                    self.rect.bottom = collider.top + 1

                    if collider in self.bouncy_obstacles:
                        self.velocity_y = self.jump_power * 1.25
                        self.set_animation("jump") 
                    else:
                        self.velocity_y = 0
                        self.on_ground = True
                        self.set_animation("idle")

                elif self.velocity_y < 0:
                    self.rect.top = collider.bottom
                    self.velocity_y = 0
                elif self.velocity_y == 0:
                    self.on_ground = True

        # Horizontal
        self.rect.x += self.velocity_x
        for collider in colliders:
            if self.rect.colliderect(collider) and self.rect.bottom != collider.top + 1:
                    if self.velocity_x > 0:
                        self.rect.right = collider.left
                    elif self.velocity_x < 0:
                        self.rect.left = collider.right
                    self.velocity_x = 0

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.move_left()
        elif keys[pygame.K_RIGHT]:
            self.move_right()
        else:
            self.stop()
            
        if keys[pygame.K_SPACE]:
            self.jump()


    def update(self, keys, dt):
        
        if not self.is_dying and not self.dead:
            self.handle_input(keys)
            self.apply_gravity()
            self.check_collisions()
            self.update_animation(dt)
        elif self.is_dying:
            self.set_animation("dead")
            self.update_animation(dt)


    def draw(self, screen, camera_offset=(0, 0)):
        draw_pos = (self.rect.x - (8 * SCALE_FACTOR) - camera_offset[0], self.rect.y - camera_offset[1])
        screen.blit(self.image, draw_pos)