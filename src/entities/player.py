# player.py
import pygame
from enum import Enum
from utils.images import extract_frames
from utils.constants import (
    MAX_FALL_SPEED,
    MOVE_SPEED,
    SCALE_FACTOR,
    MovementType,
    CAMERA_LIMITS_Y,
)

from resource_manager import ResourceManager
from sound_manager import SoundManager


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tilemap, obstacles=[]):
        super().__init__()

        # Load resources
        self.resource_manager = ResourceManager()
        self.sound_manager = SoundManager()
        sheet = self.resource_manager.load_image(
            "player_spritesheet.png", "assets\\images"
        )

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

        self.rect = pygame.Rect(x, y, 16 * SCALE_FACTOR, 32 * SCALE_FACTOR)

        # Movement & Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.running = False
        self.run_mult = 1.6
        self.jump_power = -9 * SCALE_FACTOR
        self.jumped = False
        self.lateral_jump_power = 5 * SCALE_FACTOR
        self.gravity = 0.5 * SCALE_FACTOR
        self.lateral_gravity = 0.1 * SCALE_FACTOR
        self.flipped = False
        self.on_ground = False
        self.can_glide = False
        self.position_corrected = False
        self.bouncing = False

        # Juicy stuff

        self.coyote_time = 0.3
        self._coyote_timer = 0

        self.tilemap = tilemap
        self.obstacles = obstacles
        self.is_dying = False
        self.dead = False

        self.wall_cooldown = 0

    # Movement API
    def move_left(self):
        if not self.bouncing:
            self.velocity_x = (
                -MOVE_SPEED * SCALE_FACTOR * (self.run_mult if self.running else 1)
            )
            self.flipped = True
            if self.on_ground:
                self.set_animation("walk")

        self.wall_cooldown = 0.2

    def move_right(self):
        if not self.bouncing:
            self.velocity_x = (
                MOVE_SPEED * SCALE_FACTOR * (self.run_mult if self.running else 1)
            )
            self.flipped = False
            if self.on_ground:
                self.set_animation("walk")

        self.wall_cooldown = 0.2

    def stop(self):
        if not self.bouncing:
            self.velocity_x = 0
            if self.on_ground:
                self.set_animation("idle")

    def jump(self):

        if self._coyote_timer > 0 and not self.jumped:
            self.velocity_y = self.jump_power
            self.from_ground = True
            self.set_animation("jump")
        elif self.on_wall_left and self.from_ground:
            self.flipped = False
            self.bouncing = True
            self.from_ground = False
            self.velocity_x = self.lateral_jump_power
            self.velocity_y = self.jump_power * 0.75
            self.bounce_direction = 1
            self.set_animation("jump")
        elif self.on_wall_right and self.from_ground:
            self.flipped = True
            self.bouncing = True
            self.from_ground = False
            self.velocity_x = -self.lateral_jump_power
            self.velocity_y = self.jump_power * 0.75
            self.bounce_direction = -1
            self.set_animation("jump")

        self.jumped = True

    def glide(self):
        if self.can_glide and not self.on_ground and self.velocity_y > 0:
            self.from_ground = False
            self.velocity_y = MAX_FALL_SPEED // 2
            self.set_animation("fall")

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += self.gravity
            if self.velocity_y > 0:
                self.bouncing = False
                self.set_animation("fall")
            if self.velocity_y > MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED

    def apply_lateral_gravity(self):
        if not self.on_ground and self.bouncing:
            self.velocity_x += self.lateral_gravity * (-1) * self.bounce_direction

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + (2 if self.running else 1)) % len(
                self.current_animation
            )
            if self.is_dying and self.frame_index == 5:
                self.dead = True

        new_frame = self.current_animation[self.frame_index]
        self.image = (
            pygame.transform.flip(new_frame, True, False) if self.flipped else new_frame
        )
        self.mask = pygame.mask.from_surface(self.image)

    def set_animation(self, name):
        if self.current_animation != self.animations[name]:
            self.current_animation = self.animations[name]
            self.frame_index = 0
            self.animation_timer = 0

    def check_collisions(self):

        self.on_ground = False
        colliders = self.tilemap.get_solid_rects() + self.obstacles
        platform_colliders = self.tilemap.get_platform_rects()
        self.bouncy_obstacles = self.obstacles

        old_rect = self.rect.copy()

        # Vertical
        self.rect.y += self.velocity_y
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity_y > 0:
                    self.rect.bottom = collider.top + 1
                    if collider in self.bouncy_obstacles:
                        self.velocity_y = self.jump_power * 1.25
                        self.from_ground = True
                        self.set_animation("jump")
                    else:
                        self.velocity_y = 0
                        self.bouncing = False
                        self.on_ground = True
                        self._coyote_timer = self.coyote_time
                        self.set_animation("idle")

                elif self.velocity_y < 0:
                    self.rect.top = collider.bottom
                    self.velocity_y = 0
                elif self.velocity_y == 0:
                    self.bouncing = False
                    self.on_ground = True

        for collider in platform_colliders:
            if self.rect.colliderect(collider):
                if self.velocity_y > 0 and old_rect.bottom <= collider.top:
                    self.rect.bottom = int(collider.top)
                    self.velocity_y = 0
                    self.on_ground = True
                    self._coyote_timer = self.coyote_time
                    self.set_animation("idle")

        # Horizontal
        self.rect.x += self.velocity_x
        for collider in colliders:
            if self.rect.colliderect(collider) and self.rect.bottom != collider.top + 1:
                if self.velocity_x > 0:
                    if self.bouncing:
                        self.velocity_y = 0
                    self.rect.right = collider.left - 1
                    self.bouncing = False
                    self.on_wall_right = True
                elif self.velocity_x < 0:
                    if self.bouncing:
                        self.velocity_y = 0
                    self.rect.left = collider.right + 1
                    self.bouncing = False
                    self.on_wall_left = True
                self.velocity_x = 0

    def handle_input(self, keys):

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.running = True

        else:
            self.running = False

        if keys[pygame.K_SPACE]:
            self.jump()
            self.glide()
        if keys[pygame.K_LEFT]:
            self.move_left()
        elif keys[pygame.K_RIGHT]:
            self.move_right()
        else:
            self.stop()

    def update(self, keys, dt):

        if not self.is_dying:
            self.handle_input(keys)
            self.check_collisions()
            self.apply_gravity()
            self.apply_lateral_gravity()
            self.update_animation(dt)
        else:
            self.set_animation("dead")
            self.update_animation(dt)

        if self.wall_cooldown > 0:
            self.wall_cooldown -= 1 / 60
        else:
            self.on_wall_left = False
            self.on_wall_right = False

        if self._coyote_timer > 0 and not self.on_ground:
            self._coyote_timer -= dt

        if self.on_ground:
            self.jumped = False

    def draw(self, screen, camera_offset=(0, 0)):
        draw_pos = (
            self.rect.x - (8 * SCALE_FACTOR) - camera_offset[0],
            self.rect.y - camera_offset[1],
        )
        screen.blit(self.image, draw_pos)
