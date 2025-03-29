# player.py
import os
from typing import Optional
import pygame
from utils.images import extract_frames
from utils.constants import (
    MAX_FALL_SPEED,
    MOVE_SPEED,
    SCALE_FACTOR
)

from managers.resource_manager import ResourceManager
from managers.sound_manager import SoundManager



class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        tilemap,
        obstacles: list[pygame.Rect] = [],
        camera: Optional[any] = None,
    ) -> None:
        """
        Initializes the Player object.

            :param x: Initial x position of the player.
            :param y: Initial y position of the player.
            :param tilemap: The map used for collision checks.
            :param obstacles: Additional static obstacles.
            :param camera: Optional camera reference.
        """
        super().__init__()

        # Resource managers
        self.resource_manager = ResourceManager()
        self.sound_manager = SoundManager()
        self.camera = camera

        # Load sprite sheet
        sheet = self.resource_manager.load_image(
            "player_spritesheet.png", "assets\\images"
        )

        # Extract animations from sprite sheet
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

        # Animation state
        self.current_animation = self.animations["idle"]
        self.frame_index = 0
        self.animation_speed = 0.25
        self.running_animation_speed = 0.075
        self.animation_timer = 0

        # Current frame and hitbox
        self.image = self.current_animation[self.frame_index]
        self.rect = pygame.Rect(x, y, 16 * SCALE_FACTOR, 32 * SCALE_FACTOR)

        # Movement and physics variables
        self.velocity_x = 0
        self.velocity_y = 0
        self.running = False
        self.run_mult = 1.6
        self.jump_power = -10 * SCALE_FACTOR
        self.jump_power_coyote = -6 * SCALE_FACTOR
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
        self.coyote_time = 0.3
        self._coyote_timer = 0

        # Tilemap and collision
        self.tilemap = tilemap
        self.obstacles = obstacles
        self.is_dying = False
        self.dead = False

        # Swimming and sound state
        self.is_swimming = False
        self.wall_cooldown = 0
        self.jump_sound_flag = True
        self.fall_sound_flag = False
        self.glide_sound_flag = True

        # Load footstep sounds
        self.footsteps_sound = [
            sound for sound in os.listdir("assets\\sounds\\footsteps")
        ]
        self.step_index = 0

    def move_left(self) -> None:
        """
        Moves the player to the left, flipping the sprite.
        Triggers walking animation if grounded and not swimming.
        """
        if not self.bouncing:
            self.velocity_x = -MOVE_SPEED * SCALE_FACTOR * (self.run_mult if self.running else 1)
            self.flipped = True

            if self.on_ground and not self.is_swimming:
                self.set_animation("walk")

    def move_right(self) -> None:
        """
        Moves the player to the right, unflipping the sprite.
        Triggers walking animation if grounded and not swimming.
        """
        if not self.bouncing:
            self.velocity_x = MOVE_SPEED * SCALE_FACTOR * (self.run_mult if self.running else 1)
            self.flipped = False

            if self.on_ground and not self.is_swimming:
                self.set_animation("walk")

    def stop(self) -> None:
        """
        Stops horizontal movement.
        Triggers idle animation if grounded and not swimming.
        """
        if not self.bouncing:
            self.velocity_x = 0

            if self.on_ground and not self.is_swimming:
                self.set_animation("idle")


    def jump(self) -> None:
        """
        Makes the player jump depending on the state:
        - Normal jump (coyote time)
        - Wall jump (left/right)
        - Prevents jumping if swimming

        Plays jump sound and switches animation.
        """
        if self.is_swimming:
            return  # Can't jump while swimming

        # Regular jump from ground (using coyote time)
        if self._coyote_timer > 0 and not self.jumped:
            self.velocity_y = self.jump_power_coyote
            self.from_ground = True
            self.set_animation("jump")
            self.fall_sound_flag = True

            if self.jump_sound_flag:
                self.jump_sound_flag = False
                self.sound_manager.play_sound(
                    "falling.ogg", "assets\\sounds", category="player", pan=0.5
                )

        # Wall jump from left wall
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

        # Wall jump from right wall
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

            self.jumped = True


    def glide(self) -> None:
        """
        Enables gliding if airborne, falling, and able to glide.
        Slows fall speed and plays glide animation and sound.
        """
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

    def apply_gravity(self) -> None:
        """
        Applies vertical gravity to the player.

        - If swimming: caps the fall speed.
        - If airborne: increases fall velocity up to max.
        - Also handles switching to "fall" animation.
        """
        if self.is_swimming:
            # Reduced gravity underwater
            max_swim_fall_speed = MAX_FALL_SPEED // 4
            if self.velocity_y > max_swim_fall_speed:
                self.velocity_y = max_swim_fall_speed
        elif not self.on_ground:
            # Regular gravity when in the air
            self.velocity_y += self.gravity

            # If falling and not gliding, update animation
            if self.velocity_y > 0 and not self.is_gliding:
                self.bouncing = False
                self.set_animation("fall")

            # Clamp fall speed to max allowed
            if self.velocity_y > MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED


    def apply_lateral_gravity(self) -> None:
        """
        Applies horizontal force in the opposite direction when bouncing from a wall.

        Only applies when in mid-air and not swimming.
        """
        if not self.on_ground and self.bouncing and not self.is_swimming:
            self.velocity_x += self.lateral_gravity * -1 * self.bounce_direction


    def update_animation(self, dt: float) -> None:
        """
        Updates the current animation based on time delta.

        - Uses a faster speed if running.
        - Handles footstep sounds during walking.
        - Marks player as dead when death animation finishes.
        """
        self.animation_timer += dt

        # Choose animation speed depending on whether running
        animation_speed = (
            self.running_animation_speed
            if self.current_animation == self.animations["walk"]
            else self.animation_speed
        )

        if self.animation_timer >= animation_speed:
            self.animation_timer = 0

            # Advance animation frame (faster if running)
            self.frame_index = (self.frame_index + (2 if self.running else 1)) % len(self.current_animation)

            # Check if death animation reached last frame
            if self.is_dying and self.frame_index == 5:
                self.dead = True
                self.is_dying = False

            # Play footstep sounds on specific walk frames
            if self.current_animation == self.animations["walk"] and (self.frame_index == 0 or self.frame_index == 4):
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

        # Update the sprite image (flipped if facing left)
        new_frame = self.current_animation[self.frame_index]
        self.image = (
            pygame.transform.flip(new_frame, True, False) if self.flipped else new_frame
        )
        self.mask = pygame.mask.from_surface(self.image)


    def set_animation(self, name: str) -> None:
        """
        Switches to a new animation if it's different from the current one.

        :param name: The key of the animation to set (e.g., "walk", "jump").
        """
        if self.current_animation != self.animations[name]:
            self.current_animation = self.animations[name]
            self.frame_index = 0
            self.animation_timer = 0


    def check_collisions(self) -> None:
        """
        Checks and resolves collisions against tilemap and obstacles.

        - Handles vertical and horizontal collisions.
        - Detects platforms and bouncy tiles.
        - Updates grounded and wall contact states.
        """
        # Reset collision state
        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False

        # All collision sources
        colliders = self.tilemap.get_collision_rects() + self.obstacles
        platform_colliders = self.tilemap.get_platform_rects()
        self.bouncy_obstacles = self.obstacles

        old_rect = self.rect.copy()

        # --- Vertical collision ---
        self.rect.y += self.velocity_y
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity_y > 0:
                    # Falling down: landed on something
                    self.rect.bottom = collider.top + 1

                    if collider in self.bouncy_obstacles:
                        # Bounce upward from special object
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
                        self._coyote_timer = self.coyote_time

                        if not self.is_swimming:
                            self.set_animation("idle")

                elif self.velocity_y < 0:
                    # Hitting ceiling
                    self.rect.top = collider.bottom
                    self.velocity_y = 0

                elif self.velocity_y == 0:
                    # Landed exactly on ground
                    self.bouncing = False
                    self.on_ground = True
                    self.jump_sound_flag = True
                    if self.fall_sound_flag:
                        self.fall_sound_flag = False
                        self.sound_manager.play_sound(
                            "fall.wav", "assets\\sounds", category="player", pan=0.5
                        )

        # --- Platform-specific collisions (one-way) ---
        for collider in platform_colliders:
            if self.rect.colliderect(collider):
                if self.velocity_y >= 0 and old_rect.bottom <= collider.top + 1:
                    self.rect.bottom = collider.top + 1
                    self.velocity_y = 0
                    self.on_ground = True
                    self._coyote_timer = self.coyote_time

                    self.set_animation("idle" if self.velocity_x == 0 else "walk")

        # --- Horizontal collision ---
        self.rect.x += self.velocity_x
        for collider in colliders:
            if self.rect.colliderect(collider) and self.rect.bottom != collider.top + 1:
                if self.velocity_x > 0:
                    # Hit wall on right
                    if self.bouncing:
                        self.velocity_y = 0
                    self.rect.right = collider.left - 1
                    self.bouncing = False
                    self.on_wall_right = True

                elif self.velocity_x < 0:
                    # Hit wall on left
                    if self.bouncing:
                        self.velocity_y = 0
                    self.rect.left = collider.right + 1
                    self.bouncing = False
                    self.on_wall_left = True

                self.velocity_x = 0

        # Keep player inside camera bounds (used during swimming)
        self.check_camera_bounds()


    def check_pixel_perfect_collision(self, enemy: pygame.sprite.Sprite) -> bool:
        """
        Checks pixel-perfect collision using masks.

        :param enemy: The enemy to check against.
        :returns: True if there's a pixel-perfect collision.
        """
        if enemy.mask and self.mask:
            offset = (self.rect.left - enemy.rect.left, self.rect.top - enemy.rect.top)
            return enemy.mask.overlap(self.mask, offset) is not None
        return False


    def check_camera_bounds(self) -> None:
        """
        Keeps the player within the camera's horizontal bounds.
        Only applies while swimming. Stops horizontal movement if out of bounds.
        """
        if self.is_swimming:
            left_bound, right_bound = self.camera.get_horizontal_bounds()

            if self.rect.right > right_bound:
                self.rect.right = right_bound
            elif self.rect.left < left_bound:
                self.rect.left = left_bound

            # Stop movement when out of camera bounds
            self.velocity_x = 0

    def dying(self) -> None:
        """
        Initiates the dying animation and plays sound.
        Sets is_dying flag to trigger death animation flow.
        """
        self.is_dying = True
        self.sound_manager.play_sound(
            "exhale.wav", "assets\\sounds", category="player", pan=0.5
        )

    def handle_swim_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """
        Handles swimming movement input when in water.

        :param keys: The current state of keyboard keys.
        """
        self.set_animation("swim")

        if keys[pygame.K_UP]:
            self.velocity_y = self.swim_ascend_speed
        elif keys[pygame.K_DOWN]:
            self.velocity_y += self.swim_gravity * 10
        else:
            self.velocity_y += self.swim_gravity


    def climb_stairs(self) -> None:
        """
        Handles stair climbing when the player overlaps with stair tiles.
        Moves the player slightly upward and disables normal grounded states.
        """
        stairs_colliders = self.tilemap.get_stairs_rects()

        for collider in stairs_colliders:
            if self.rect.colliderect(collider):
                self.rect.y -= 2  # Move the player up slightly

                # Reset movement and state flags
                self.velocity_x = 0
                self.velocity_y = 0
                self.on_ground = False
                self.on_wall_left = False
                self.on_wall_right = False
                self.can_glide = False
                self.position_corrected = True


    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """
        Interprets player input to control movement, jumping, gliding, and climbing.

        :keys: The current state of keyboard keys.
        """
        if self.is_swimming:
            self.handle_swim_input(keys)
        else:
            if keys[pygame.K_SPACE]:
                self.jump()
                self.glide()
            else:
                # Reset gliding state when not holding jump
                self.is_gliding = False
                self.glide_sound_flag = True

        # Check for stair climbing
        if keys[pygame.K_UP]:
            self.climb_stairs()

        # Handle running
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and not self.is_swimming:
            self.running = True
        else:
            self.running = False

        # Handle left/right movement
        if keys[pygame.K_LEFT]:
            self.move_left()
        elif keys[pygame.K_RIGHT]:
            self.move_right()
        else:
            self.stop()

    def update(self, keys: pygame.key.ScancodeWrapper, dt: float) -> None:
        """
        Updates the player's state every frame.

        :keys: Pressed keys this frame.
        :dt: Delta time since last frame.
        """
        if not self.is_dying and not self.dead:
            self.handle_input(keys)
            self.check_collisions()
            self.apply_gravity()
            self.apply_lateral_gravity()
            self.update_animation(dt)
        else:
            self.set_animation("dead")
            self.update_animation(dt)

        # Coyote time countdown if not on ground
        if self._coyote_timer > 0 and not self.on_ground:
            self._coyote_timer -= dt

        # Reset jump state if grounded
        if self.on_ground:
            self.jumped = False


    def draw(self, screen: pygame.Surface, camera_offset: tuple[int, int] = (0, 0)) -> None:
        """
        Renders the player on the screen with camera offset.

        :param screen: The surface to draw on.
        :param camera_offset: The (x, y) offset from the camera position.
        """
        if not self.dead:
            draw_pos = (
                self.rect.x - (8 * SCALE_FACTOR) - camera_offset[0],
                self.rect.y - camera_offset[1],
            )
            screen.blit(self.image, draw_pos)

