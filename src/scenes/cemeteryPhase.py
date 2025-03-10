import pygame
from enviorement.tilemap import Tilemap
from scenes.phase import Phase 
from utils.constants import WIDTH, HEIGHT
from enviorement.background import Background
from resource_manager import ResourceManager
from sound_manager import SoundManager
from entities.player import Player
from enviorement.camera import Camera
from entities.gravedigger import Gravedigger


class CemeteryPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.foreground = Tilemap("tiled/levels/test_level.tmx")
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.background = Background(self.resources, "assets\\images\\backgrounds\\parallax_forest")
        self.player = Player(0, WIDTH//2, self.foreground)
        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}
        #gravedigger_spawn = tilemap.entities.get("enemy_spawn")
        #gravedigger = Gravedigger(gravedigger_spawn.x, gravedigger_spawn.y, tilemap)

        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)

    def update(self):
        dt = self.director.clock.get_time() / 1000

        # Actualización del jugador con input y tiempo
        self.player.update(self.pressed_keys, dt)

        # Si murió, cambio de escena
        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")

        # Actualizar cámara (ahora solo con el rect del jugador)
        self.camera.update(self.player.rect)

        # Foreground y background deberían actualizarse solo si tienen lógica propia (ej: animaciones)
        #self.foreground.update()
        self.background.update(0)

    def draw(self):
        # Obtener offset de cámara para desplazar todo al dibujar
        offset = self.camera.get_offset()

        print(offset)

        # Dibujo con offset
        self.background.draw(self.screen)
        self.foreground.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
    