from time import sleep
import pygame
from enviorement.tilemap import Tilemap
from entities.lantern import Lantern
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

        path_points = {}

        for obj in self.foreground.tmx_data.objects:
            if obj.type == "Point":
                path_points[int(obj.name)] = (obj.x, obj.y)
                print(path_points)

        # Ordenar los puntos por su índice y devolverlos como lista
        path_points = [path_points[i] for i in sorted(path_points.keys())]
        self.lantern = Lantern(position=path_points[0], path=path_points, speed=5)

        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)

        self.foreground.insert_sprite(self.player, 2)
        self.foreground.insert_sprite(self.lantern, -1)

    index = 0

    def update(self):
        dt = self.director.clock.get_time() / 1000

        self.player.update(self.pressed_keys, dt)
        self.lantern.update(self.player, self.foreground, self.camera.get_offset())
        if self.player.dead:
            self.director.scene_manager.stack_scene("DyingMenu")

        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
