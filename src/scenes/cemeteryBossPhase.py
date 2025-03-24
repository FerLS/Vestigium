from time import sleep
import pygame
from enviorement.tilemap import Tilemap
from light2 import CircularLight, ConeLight
from scenes.phase import Phase
from utils.constants import WIDTH, HEIGHT
from enviorement.background import Background
from resource_manager import ResourceManager
from sound_manager import SoundManager
from entities.player import Player
from enviorement.camera import Camera
from entities.gravedigger import Gravedigger
from entities.firefly import Firefly
from entities.mushroom import Mushroom


class CemeteryBossPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.foreground = Tilemap("tiled/levels/cementery_boss.tmx")
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.background = Background(
            self.resources, "assets\\images\\backgrounds\\parallax_forest"
        )

        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}
        # Player

        player_spawn = self.foreground.load_entity("player_spawn")
        self.player = Player(player_spawn.x, player_spawn.y, self.foreground)

        # Lantern

        self.lantern_light = ConeLight(
            self.player.rect.center, 10, 70, 100, segments=30
        )

        self.lantern_position = (
            self.player.rect.center
        )  # Puedes ajustar esto según sea necesario
        self.lantern_direction = "right"  # Dirección inicial de movimiento

        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)

    index = 0

    def update(self):
        dt = self.director.clock.get_time() / 1000

        self.player.update(self.pressed_keys, dt)

        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")

        # Actualiza la posición de la linterna en función de la dirección
        if self.lantern_direction == "right":
            self.lantern_position = (
                self.lantern_position[0] + 1,  # Ajusta la velocidad de movimiento aquí
                self.lantern_position[1],
            )
            # Cambia de dirección si llega al borde derecho del mapa
            if self.lantern_position[0] >= WIDTH:
                self.lantern_direction = "left"
        elif self.lantern_direction == "left":
            self.lantern_position = (
                self.lantern_position[0] - 1,  # Ajusta la velocidad de movimiento aquí
                self.lantern_position[1],
            )
            # Cambia de dirección si llega al borde izquierdo del mapa
            if self.lantern_position[0] <= 0:
                self.lantern_direction = "right"

        # Actualiza la luz de la linterna con la nueva posición
        self.lantern_light.update(
            new_position=self.lantern_position,
            obstacles=self.foreground.get_solid_rects()
            + self.foreground.get_platform_rects(),
        )

        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
        self.lantern_light.draw(self.screen, offset)
