# player.py
import os
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
    def __init__(self, x, y, tilemap, obstacles, camera=None, light=None):
        super().__init__()

        self.light = light

        # Load resources
        self.resource_manager = ResourceManager()
        self.sound_manager = SoundManager()
        sheet = self.resource_manager.load_image(
            "player_spritesheet.png", "assets\\images"
        )
        self.camera = camera

        # Animations
        self.animations = {
            "idle": extract_frames(sheet, 0, 0, 32, 32, 2, SCALE_FACTOR)
            + extract_frames(sheet, 0, 32, 32, 32, 2, SCALE_FACTOR),
            "walk": extract_frames(sheet, 0, 96, 32, 32, 8, SCALE_FACTOR),
            "jump": extract_frames(sheet, 0, 160, 32, 32, 8, SCALE_FACTOR),
            "fall": extract_frames(sheet, 128, 160, 32, 32, 1, SCALE_FACTOR),
            "glide": extract_frames(sheet, 0, 224, 32, 32, 1, SCALE_FACTOR),
            "dead": extract_frames(sheet, 0, 192, 32, 32, 6, SCALE_FACTOR),
            "swim": extract_frames(sheet, 0, 160, 32, 32, 8, SCALE_FACTOR, lying=-10.0),
        }

        self.current_animation = self.animations["idle"]
        self.frame_index = 0
        self.animation_speed = 0.25
        self.running_animation_speed = 0.075
        self.animation_timer = 0

        self.image = self.current_animation[self.frame_index]

        self.rect = pygame.Rect(x, y, 16 * SCALE_FACTOR, 32 * SCALE_FACTOR)

        # Movement & Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.running = False
        self.run_mult = 1.6
        self.jump_power = -10 * SCALE_FACTOR
        self.jumped = False
        self.lateral_jump_power = 5 * SCALE_FACTOR
        self.gravity = 0.5 * SCALE_FACTOR
        self.lateral_gravity = 0.1 * SCALE_FACTOR
        self.swim_gravity = 0.2 * SCALE_FACTOR
        self.swim_ascend_speed = -3 * SCALE_FACTOR
        self.flipped = False
        self.on_ground = False
        self.can_glide = False
        self.is_gliding = False
        self.bouncing = False
        self.position_corrected = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.from_ground = False
        self._coyote_timer = 0

        self.tilemap = tilemap
        self.obstacles = obstacles
        self.is_dying = False
        self.dead = False

        self.is_swimming = False
        self.wall_cooldown = 0
        self.jump_sound_flag = True
        self.fall_sound_flag = False
        self.glide_sound_flag = True

        # Sounds
        self.footsteps_sound = [
            sound for sound in os.listdir("assets\\sounds\\footsteps")
        ]
        self.step_index = 0

    def move_left(self):
        if not self.bouncing:
            self.velocity_x = (
                -MOVE_SPEED * SCALE_FACTOR * (self.run_mult if self.running else 1)
            )
            self.flipped = True
            if self.on_ground and not self.is_swimming:
                self.set_animation("walk")

        self.wall_cooldown = 0.2

    def move_right(self):
        if not self.bouncing:
            self.velocity_x = (
                MOVE_SPEED * SCALE_FACTOR * (self.run_mult if self.running else 1)
            )
            self.flipped = False
            if self.on_ground and not self.is_swimming:
                self.set_animation("walk")

        self.wall_cooldown = 0.2

    def stop(self):
        if not self.bouncing:
            self.velocity_x = 0
            if self.on_ground and not self.is_swimming:
                self.set_animation("idle")

    def jump(self):
        if self.is_swimming:
            return
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.from_ground = True
            self.set_animation("jump")

            self.fall_sound_flag = True

            if self.jump_sound_flag:
                self.jump_sound_flag = False
                self.sound_manager.play_sound(
                    "falling.ogg", "assets\\sounds", category="player", pan=0.5
                )

        elif self.on_wall_left and self.from_ground:
            self.flipped = False
            self.bouncing = True
            self.from_ground = False
            self.velocity_x = self.lateral_jump_power
            self.velocity_y = self.jump_power * 0.75
            self.bounce_direction = 1
            self.set_animation("jump")
            self.fall_sound_flag = True

            if self.jump_sound_flag:
                self.jump_sound_flag = False
                self.sound_manager.play_sound(
                    "falling.ogg", "assets\\sounds", category="player", pan=0.5
                )
        elif self.on_wall_right and self.from_ground:
            self.flipped = True
            self.bouncing = True
            self.from_ground = False
            self.velocity_x = -self.lateral_jump_power
            self.velocity_y = self.jump_power * 0.75
            self.bounce_direction = -1
            self.set_animation("jump")
            self.fall_sound_flag = True

            if self.jump_sound_flag:
                self.jump_sound_flag = False
                self.sound_manager.play_sound(
                    "falling.ogg", "assets\\sounds", category="player", pan=0.5
                )

    def glide(self):
        if (
            self.can_glide
            and not self.is_swimming
            and not self.on_ground
            and self.velocity_y > 0
        ):
            self.from_ground = False
            self.velocity_y = MAX_FALL_SPEED // 2
            self.is_gliding = True
            self.set_animation("glide")
            if self.glide_sound_flag:
                self.glide_sound_flag = False
                self.sound_manager.play_sound(
                    "falling.ogg", "assets\\sounds", category="player", pan=0.5
                )

    def apply_gravity(self):
        if self.is_swimming:
            max_swim_fall_speed = MAX_FALL_SPEED // 4
            if self.velocity_y > max_swim_fall_speed:
                self.velocity_y = max_swim_fall_speed
        else:
            if not self.on_ground:
                self.velocity_y += self.gravity
                if self.velocity_y > 0 and not self.is_gliding:
                    self.bouncing = False
                    self.set_animation("fall")
                if self.velocity_y > MAX_FALL_SPEED:
                    self.velocity_y = MAX_FALL_SPEED

    def apply_lateral_gravity(self):
        if not self.on_ground and self.bouncing and not self.is_swimming:
            self.velocity_x += self.lateral_gravity * (-1) * self.bounce_direction

    def update_animation(self, dt):

        self.animation_timer += dt
        animation_speed = (
            self.running_animation_speed
            if self.current_animation == self.animations["walk"]
            else self.animation_speed
        )

        if self.animation_timer >= animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + (2 if self.running else 1)) % len(
                self.current_animation
            )
            if self.is_dying and self.frame_index == 5:
                self.dead = True
                self.is_dying = False

            if self.current_animation == self.animations["walk"] and (
                self.frame_index == 0 or self.frame_index == 4
            ):
                if self.velocity_x > 0:
                    self.sound_manager.play_sound(
                        self.footsteps_sound[self.step_index],
                        "assets\\sounds\\footsteps",
                        category="player",
                        pan=0.7,
                    )
                elif self.velocity_x < 0:
                    self.sound_manager.play_sound(
                        self.footsteps_sound[self.step_index],
                        "assets\\sounds\\footsteps",
                        category="player",
                        pan=0.3,
                    )
                self.step_index = 1 - self.step_index

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
        colliders = self.tilemap.get_collision_rects()
        self.bouncy_obstacles = self.obstacles
        colliders += self.obstacles

        self.rect.y += self.velocity_y
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity_y > 0:
                    self.rect.bottom = collider.top + 1
                    if collider in self.bouncy_obstacles:
                        self.velocity_y = self.jump_power * 1.25
                        self.from_ground = True
                        self.set_animation("jump")
                        self.sound_manager.play_sound(
                            "falling.ogg", "assets\\sounds", category="player", pan=0.5
                        )
                    else:
                        self.velocity_y = 0
                        self.bouncing = False
                        self.on_ground = True
                        if not self.is_swimming:
                            self.set_animation("idle")
                elif self.velocity_y < 0:
                    self.rect.top = collider.bottom
                    self.velocity_y = 0
                elif self.velocity_y == 0:
                    self.bouncing = False
                    self.on_ground = True
                    self.jump_sound_flag = True
                    if self.fall_sound_flag:
                        self.fall_sound_flag = False
                        self.sound_manager.play_sound(
                            "fall.wav", "assets\\sounds", category="player", pan=0.5
                        )

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

        self.check_camera_bounds()  # Check if the player is out of the camera bounds

    def check_pixel_perfect_collision(self, enemy):
        if enemy.mask and self.mask:
            offset = (self.rect.left - enemy.rect.left, self.rect.top - enemy.rect.top)
            if enemy.mask.overlap(self.mask, offset):
                return True

    def check_camera_bounds(self):
        """Check if the player is out of the camera bounds at lake phase"""
        if self.is_swimming:
            left_bound, right_bound = self.camera.get_horizontal_bounds()

            if self.rect.right > right_bound:
                self.rect.right = right_bound
            elif self.rect.left < left_bound:
                self.rect.left = left_bound
            self.velocity_x = 0

    def dying(self):
        self.is_dying = True
        self.sound_manager.play_sound(
            "exhale.wav", "assets\\sounds", category="player", pan=0.5
        )

    def handle_swim_input(self, keys):
        self.set_animation("swim")
        if keys[pygame.K_UP]:
            self.velocity_y = self.swim_ascend_speed
        elif keys[pygame.K_DOWN]:
            self.velocity_y += self.swim_gravity * 10
        else:
            self.velocity_y += self.swim_gravity

    def handle_input(self, keys):
        if self.is_swimming:
            self.handle_swim_input(keys)
        else:
            if keys[pygame.K_SPACE]:
                self.jump()
                self.glide()
            else:
                self.is_gliding = False
                self.glide_sound_flag = True

        if keys[pygame.K_LEFT]:
            self.move_left()
        elif keys[pygame.K_RIGHT]:
            self.move_right()
        else:
            self.stop()

    def update(self, keys, dt):
        if not self.is_dying and not self.dead: # Si estou morrendo ou morto non fago nada mentras
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
        if not self.dead:
            draw_pos = (
                self.rect.x - (8 * SCALE_FACTOR) - camera_offset[0],
                self.rect.y - camera_offset[1],
            )
            screen.blit(self.image, draw_pos)
