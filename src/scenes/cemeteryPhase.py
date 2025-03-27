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
from entities.firefly import Firefly
from entities.mushroom import Mushroom
from trigger import Trigger
from scenes.fadeTransition import FadeTransition, FadeIn, FadeOut


class CemeteryPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.foreground = Tilemap("tiled/levels/test_level.tmx")
        self.resources = ResourceManager()
        self.sound_manager = SoundManager()
        self.background = Background(
            self.resources, "assets\\images\\backgrounds\\parallax_forest"
        )

        self.camera = Camera(WIDTH, HEIGHT)
        self.pressed_keys = {}
        area_rect = pygame.Rect(500, 500, 300, 200)
        # gravedigger_spawn = tilemap.entities.get("enemy_spawn")
        # gravedigger = Gravedigger(gravedigger_spawn.x, gravedigger_spawn.y, tilemap)

        self.firefly = Firefly(600, 600, area_rect)
        self.mushroom = Mushroom(100, 800)
        self.lights_group = pygame.sprite.Group(self.firefly.light, self.mushroom.light)
        self.mushrooms_group = pygame.sprite.Group(self.mushroom)
        obstacles = [mushroom.platform_rect for mushroom in self.mushrooms_group]

        # Triggers
        self.triggers = []
        end_coords = self.foreground.load_entity("cemetery_end")
        self.end_phase_rect = pygame.Rect(end_coords.x, end_coords.y, end_coords.width, end_coords.height)
        end_phase_trigger = Trigger(self.end_phase_rect, lambda: self.fade_out.start())
        self.triggers.append(end_phase_trigger)

        self.spawns_rects = [pygame.Rect(v.x, v.y, v.width, v.height) for v in self.foreground.load_layer_entities("checkpoints").values()]
        for spawn_rect in self.spawns_rects:
            self.triggers.append(Trigger(spawn_rect, self.increment_spawn_index))
        self.spawn_index = 0
        self.current_spawn = self.spawns_rects[self.spawn_index].center
        self.player = Player(self.current_spawn[0], self.current_spawn[1], self.foreground , obstacles)

        self.sound_manager.play_music("mystic_forest.mp3", "assets\\music", -1)

        # Fades
        self.fades = {}
        fade_in = FadeIn(self.screen)
        fade_in.start()
        self.fades['fade_in'] = fade_in


        fade_out = FadeOut(self.screen, on_complete= lambda: self.end_of_phase("TreePhase"))
        self.fades['fade_out'] = fade_out

        revive_fade_in = FadeIn(self.screen, duration=2, on_complete=lambda: self.revive_player())
        self.fades['revive_fade_in'] = revive_fade_in
        death_fade_out = FadeOut(self.screen, duration=2, on_complete=lambda:  self.fades['revive_fade_in'].start())
        self.fades['death_fade_out'] = death_fade_out      

    def increment_spawn_index(self):
        self.spawn_index += 1
    
    def revive_player(self):
        self.player.rect.center = self.current_spawn
        self.player.dead = False
        

    def update(self):
        dt = self.director.clock.get_time() / 1000

        self.player.update(self.pressed_keys, dt)
        self.firefly.update()
        self.mushroom.update()

        for mushroom in self.mushrooms_group:
            if self.player.rect.colliderect(mushroom.platform_rect):
                mushroom.glow = True
                mushroom.bounce = True

        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)
        
        for fade in self.fades.values():
            fade.update(dt)

        if pygame.sprite.spritecollideany(self.player, self.lights_group) and not self.player.is_dying and not self.player.dead:
            print("colliding")
            self.player.dying()
            self.fades['death_fade_out'].start()
           
        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
        self.mushroom.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
        self.firefly.draw(self.screen, offset)
        for fade in self.fades.values():
            fade.draw()

    def continue_procedure(self):
        pass

    def end_of_phase(self, phase: str):
        self.director.scene_manager.change_scene(phase)
