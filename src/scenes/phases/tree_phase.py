import pygame
from entities.players.player import Player
from entities.npcs.mushroom import Mushroom
from entities.npcs.spider import Spider
from entities.npcs.firefly import Firefly
from gui.gui_elements.gui_text import CheckpointText, GlideInstructionText
from utils.light import ConeLight
from scenes.phase import Phase

class TreePhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen = director.screen
        self.pressed_keys = {}

        self.load_resources(
            tilemap_path="tiled/levels/tree.tmx",
            background_path="assets\\images\\backgrounds\\tree_phase_parallax",
            enable_vertical_scroll=True
            )
        self.setup_camera()
        self.setup_groups()
        self.setup_spawns()
        self.setup_enemies()
        self.setup_player()
        self.setup_triggers()
        self.setup_fades(scene_name="LakePhase")
        self.setup_audio(
            music_name="tree_music.mp3",
            sound_name="forest_ambient.wav"
            )
        
    def setup_groups(self):
        """
        Setup the sprite groups and trigger list for the scene.
        """
        self.lights_group = pygame.sprite.Group()
        self.pixel_perfect_lights_group = pygame.sprite.Group()
        self.mushrooms_group = pygame.sprite.Group()
        self.spiders_group = pygame.sprite.Group()
        self.fireflies_group = pygame.sprite.Group()
        self.bouncy_obstacles = []
        self.triggers = []
        self.fades = {}

    def setup_audio(self):
        """
        Setup the audio for the scene.
        """
        self.sound_manager.play_music("tree_music.mp3", "assets\\music", -1)
        self.sound_manager.play_sound("forest_ambient.wav", "assets\\sounds", category='ambient', loop=True)

    def setup_spawns(self):
        """
        Setup the spawn points for the scene.
        """
        self.spawns_rects = [pygame.Rect(v.x, v.y, v.width, v.height) for v in self.foreground.load_layer_entities("checkpoints").values()]
        for spawn_rect in self.spawns_rects:
            self.triggers.append(Trigger(spawn_rect, lambda: self.increment_spawn_index()))
        for i, spawn_rect in enumerate(self.spawns_rects):
            if i in [1, 2, 3]:
                self.triggers.append(Trigger(spawn_rect, lambda: self.show_respawn_text()))
        self.spawn_index = -1
        self.current_spawn = self.spawns_rects[self.spawn_index].center

    def setup_player(self):
        """
        Create the player entity.
        """
        player_spawn = self.spawns_rects[0].center
        self.player = Player(player_spawn[0], player_spawn[1], 
                             self.foreground, 
                             obstacles=self.bouncy_obstacles)

    def setup_enemies(self):
        """
        Setup the entities for the scene.
        """
        self.load_mushrooms()
        self.load_spiders()
        self.load_fireflies()
        self.load_static_lights()

    def load_mushrooms(self):
        """
        Place the mushrooms in the scene and add them to the groups.
        """
        mushrooms = self.foreground.load_layer_entities("mushrooms")
        for data in mushrooms.values():
            mushroom = Mushroom(data.x, data.y)
            self.bouncy_obstacles.append(mushroom.platform_rect)
            self.mushrooms_group.add(mushroom)
            self.lights_group.add(mushroom.light)

    def load_spiders(self):
        """
        Place the spiders in the scene and add them to the groups.
        """
        spiders = self.foreground.load_layer_entities("spiders")
        for spider in spiders.values():
            spider = Spider(spider.x, spider.y)
            self.spiders_group.add(spider)
            self.lights_group.add(spider.light)

    def load_fireflies(self):
        """
        Place the fireflies in the scene and add them to the groups.
        """
        fireflies = self.foreground.load_layer_entities("fireflies")
        bounds = self.foreground.load_entity("movement_bounds")
        movement_bounds = pygame.Rect(bounds.x, bounds.y, bounds.width, bounds.height)
        for data in fireflies.values():
            firefly = Firefly(data.x, data.y, movement_bounds)
            self.fireflies_group.add(firefly)
            self.lights_group.add(firefly.light)

    def load_static_lights(self):
        """
        Place the static lights in the scene and add them to the pixel perfect light group to perform collision with mask.
        """
        self.hide_lights = False
        left_lights = self.foreground.load_layer_entities("left_lights")
        for light in left_lights.values():
            self.pixel_perfect_lights_group.add(
                ConeLight((light.x, light.y), pygame.Vector2(1, 1), 30, 500, segments=10, ray_step=4)
            ) 

        right_lights = self.foreground.load_layer_entities("right_lights")
        for light in right_lights.values():
            self.pixel_perfect_lights_group.add(
                ConeLight((light.x, light.y), pygame.Vector2(-1, 0.6), 30, 500, segments=10, ray_step=4)
            )

    def setup_triggers(self):
        """
        Setup the triggers for the scene.
        """
        self.init_trigger("glide_trigger", lambda: self.glide())
        self.init_trigger("camera_y_margin_trigger", lambda: self.change_camera_y_margin(self.camera.screen_height // 2.2))
        self.init_trigger("end_of_phase", lambda: self.fades['fade_out'].start())

    def init_trigger(self, entity_name: str, callback: callable):
        """
        Initialize a trigger with a callback function.
        """
        entity = self.foreground.load_entity(entity_name)
        trigger_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        self.triggers.append(Trigger(trigger_rect, callback))

    def setup_fades(self):
        """
        Setup all fade effects for the scene.
        """
        fade_in = FadeIn(self.screen)
        fade_in.start()
        self.fades['fade_in'] = fade_in

        fade_out = FadeOut(self.screen, on_complete=lambda: self.end_of_phase("LakePhase"))
        self.fades['fade_out'] = fade_out

        revive_fade_in = FadeIn(self.screen, duration=2, on_complete=lambda: self.revive_player())
        self.fades['revive_fade_in'] = revive_fade_in

        death_fade_out = FadeOut(self.screen, duration=2, on_complete=lambda: self.move_player_to_spawn())
        self.fades['death_fade_out'] = death_fade_out

    def increment_spawn_index(self):
        """
        Increment the spawn index.
        """
        self.spawn_index += 1
        self.current_spawn = self.spawns_rects[self.spawn_index].center
        
    def show_respawn_text(self):
        text = CheckpointText(self.screen, (100, 50))
        return text

    def update(self):
        dt = self.director.clock.get_time() / 1000

        # Update player and entities
        self.player.update(self.pressed_keys, dt)

        self.mushrooms_group.update()

        self.spiders_group.update(dt)

        self.fireflies_group.update()

        # Check if the player is colliding with the mushrooms
        for mushroom in self.mushrooms_group:
            if self.player.rect.colliderect(mushroom.platform_rect):
                mushroom.glow = True
                mushroom.bounce = True

        # Check pixel perfect collision of lights and obstacles 
        spider_rects = [spider.rect for spider in self.spiders_group]
        self.collidable_obstacles = self.foreground.get_collision_rects() + self.bouncy_obstacles + spider_rects
        self.pixel_perfect_lights_group.update(obstacles=self.collidable_obstacles, camera_rect=self.camera.get_view_rect())

        # Check if the player is colliding with the pixel perfect collisions
        if any(self.player.check_pixel_perfect_collision(light) for light in self.pixel_perfect_lights_group) and not self.player.is_dying and not self.player.dead:
            self.player.dying()            
            self.fades['death_fade_out'].start()

        # Check if the player is colliding with lights with rects
        if pygame.sprite.spritecollideany(self.player, self.lights_group) and not self.player.is_dying and not self.player.dead:
            self.player.dying()
            self.fades['death_fade_out'].start()

        # Update and check triggers
        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)
        
        # Update fade effects
        for fade in self.fades.values():
            fade.update(dt)

        # Update camera
        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)

        self.foreground.draw(self.screen, offset)

        # Draw pixel perfect lights (lights of enemies are drawn in their respective draw method)
        for light in self.pixel_perfect_lights_group:
            if not self.hide_lights:
                light.draw(self.screen, offset)

        # Draw entities
        for group in [self.mushrooms_group, self.spiders_group, self.fireflies_group]:
            for entity in group:
                entity.draw(self.screen, offset)

        self.player.draw(self.screen, camera_offset=offset)

        # Draw triggers text if it exists
        for trigger in self.triggers:
            trigger.draw(self.screen)

        # Draw fade out transition
        for fade in self.fades.values():
            fade.draw()

    def continue_procedure(self):
        self.sound_manager.play_sound("forest_ambient.wav", "assets\\sounds", category='ambient', loop=True)

    # Actions that can be triggered by a Trigger
    def glide(self):
        """
        Enable the player to glide and display the instruction text.
        """
        text = GlideInstructionText(self.screen, (100, 100))
        self.player.can_glide = True
        self.hide_lights = True
        return text

    def change_camera_y_margin(self, new_margin: int):
        """
        Change the y margin of the camera.
        """
        self.camera.margin_y = new_margin
        return None

    def end_of_phase(self, scene: str):
        """
        Change the scene to the next phase.
        """
        self.sound_manager.play_sound("water-splash.ogg", "assets\\sounds", category='ambient')
        self.director.scene_manager.change_scene(scene)
        return None
