import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, scale_factor=3):
        super().__init__()

        # Configuración de animaciones
        self.animations_config = {
            "idle": {"row": 0, "frames": 6, "size": (24, 24)},
            "walk": {"row": 1, "frames": 8, "size": (24, 24)},
            "jump": {"row": 2, "frames": 4, "size": (24, 24)},
            "fall": {"row": 3, "frames": 3, "size": (24, 24)},
        }

        # Configuración física
        self.physics = {
            "gravity": 0.8,
            "jump_strength": -23,
            "speed": 4,
        }

        # Estados iniciales
        self.direction = 1  # 1 = derecha, -1 = izquierda
        self.current_animation = "idle"
        self.is_jumping = False
        self.on_ground = False
        self.y_velocity = 0

        # Añadir estas propiedades
        self.jump_cooldown = 100  # ms entre saltos
        self.last_jump_time = 0

        # Carga de recursos
        self.spritesheet = self._load_spritesheet()
        self.animation_frames = self._load_animation_frames(scale_factor)

        # Configuración de sprite
        self.image = self.animation_frames[self.current_animation][0]
        self.rect = self.image.get_rect(topleft=(100, 100))

        # Temporización de animación
        self.animation_speed = 0.1  # segundos por frame
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()

        self.mask = pygame.mask.from_surface(self.image)

    def _load_spritesheet(self):
        return pygame.image.load(
            os.path.join("assets", "images", "Player_anim_Sheet.png")
        ).convert_alpha()

    def _load_animation_frames(self, scale_factor):
        frames_dict = {}
        for name, config in self.animations_config.items():
            frames = []
            width, height = config["size"]

            for frame in range(config["frames"]):
                x = frame * width
                y = config["row"] * height

                # Extraer frame del spritesheet
                frame_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                frame_surf.blit(self.spritesheet, (0, 0), (x, y, width, height))

                # Escalar y guardar frame
                scaled_size = (width * scale_factor, height * scale_factor)
                frames.append(pygame.transform.scale(frame_surf, scaled_size))

            frames_dict[name] = frames
        return frames_dict

    def _handle_animation_transition(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now

            # No avanzar en últimos frames de salto/caída
            if self.current_animation in ("jump", "fall"):
                if (
                    self.frame_index
                    == len(self.animation_frames[self.current_animation]) - 1
                ):
                    return

            self.frame_index = (self.frame_index + 1) % len(
                self.animation_frames[self.current_animation]
            )

            # Aplicar dirección
            self.image = self.animation_frames[self.current_animation][self.frame_index]
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

    def _update_state(self, actions):
        # Determinar dirección
        if actions["left"]:
            self.direction = -1
        elif actions["right"]:
            self.direction = 1

        # Prioridad de estados
        if actions["jump"]:
            self.current_animation = "jump"
            self.is_jumping = True
            self.frame_index = 0
        elif self.is_jumping:
            return  # Mantener estado de salto
        elif actions["left"] or actions["right"]:
            self.current_animation = "walk"
        else:
            self.current_animation = "idle"

            self.mask = pygame.mask.from_surface(self.image)

    def _apply_physics(self, actions, ground_group):
        # Movimiento horizontal
        self.rect.x += (actions["right"] - actions["left"]) * self.physics["speed"]

        # Aplicar gravedad
        self.y_velocity += self.physics["gravity"]
        self.rect.y += self.y_velocity

        # Detectar colisiones verticales
        self.on_ground = False
        for platform in pygame.sprite.spritecollide(self, ground_group, False):
            if self.y_velocity > 0:  # Colisión hacia abajo
                if self.rect.bottom > platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.y_velocity = 0
                    self.on_ground = True
            elif self.y_velocity < 0:  # Colisión hacia arriba
                self.rect.top = platform.rect.bottom
                self.y_velocity = 0

        # Manejar salto
        now = pygame.time.get_ticks()
        if (
            actions["jump"]
            and self.on_ground
            and now - self.last_jump_time > self.jump_cooldown
        ):
            self.y_velocity = self.physics["jump_strength"]
            self.on_ground = False
            self.last_jump_time = now

        # Actualizar animación
        if not self.on_ground:
            self.current_animation = "fall" if self.y_velocity > 0 else "jump"
        else:
            if actions["left"] or actions["right"]:
                self.current_animation = "walk"
            else:
                self.current_animation = "idle"

    def update(self, actions, ground_group):
        actions = {
            "left": int(actions["left"]),
            "right": int(actions["right"]),
            "jump": int(actions["jump"]),
        }

        self._update_state(actions)
        self._apply_physics(actions, ground_group)
        self._handle_animation_transition()
