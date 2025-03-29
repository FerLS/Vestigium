import pygame
from gui.gui_elements.gui_text import CheckpointText, InitialInstructionText, RetryInstructionText
from scenes.phase import Phase
from entities.players.player import Player
from entities.npcs.firefly import Firefly
from utils.light import ConeLight 



class CemeteryPhase(Phase):
    def __init__(self, director):
        super().__init__(director)
        self.screen: pygame.Surface = director.screen
        self.pressed_keys: dict = {}
                        
        self.load_resources(tilemap_path="tiled/levels/cemetery.tmx",
                            background_path="assets\\images\\backgrounds\\cemetery_phase_background")
        self.setup_camera()
        self.setup_instructions()
        self.setup_groups()
        self.setup_spawns(respawn_text_spawns = [1, 2])
        self.setup_player()
        self.setup_enemies()
        self.setup_triggers()
        self.setup_fades(scene_name="CemeteryBossPhase")
        self.setup_audio(music_name="cemetery_music.mp3",
                         sound_name="cemetery_background_sound.ogg")
        
    def setup_instructions(self):
        """
        Setup the instruction text for the scene.
        """
        self.instruction_text = InitialInstructionText(self.screen, (100, 100))
    
    def setup_groups(self):
        """
        Setup the sprite groups and trigger list for the scene.
        """
        self.lampposts_group = pygame.sprite.Group()
        self.lights_group = pygame.sprite.Group()
        self.fireflies_group = pygame.sprite.Group()
        self.triggers = []

    def setup_player(self):
        """
        Create the player entity.
        """
        player_spawn = self.spawns_rects[0].center
        self.player = Player(player_spawn[0], player_spawn[1], 
                             self.foreground, 
                             obstacles=[])
      
    def revive_player(self):
        """
        Show instructions and revive the player after dying.
        """
        self.instruction_text = RetryInstructionText(self.screen, (50, 100))
        super().revive_player()

    def increment_spawn_index(self):
        """
        Increment the spawn index and show dying instructions.
        """
        self.instruction_text.visible = True
        super().increment_spawn_index()
        
    def setup_enemies(self):
        """
        Setup the entities for the scene.
        """
        # Lampposts
        self.create_lampposts()
        
        # Vertical fireflies
        fireflies = self.foreground.load_layer_entities("fireflies_v")
        for firefly in fireflies.values():
            firefly = Firefly(firefly.x, firefly.y, movement_type="vertical")
            self.fireflies_group.add(firefly)
            self.lights_group.add(firefly.light)
        
        # Horizontal fireflies
        fireflies = self.foreground.load_layer_entities("fireflies_h")
        for firefly in fireflies.values():
            firefly = Firefly(firefly.x, firefly.y,movement_type="horizontal")
            self.fireflies_group.add(firefly)
            self.lights_group.add(firefly.light)
        
    def setup_player(self):
        """
        Create the player entity.
        """
        player_spawn = self.spawns_rects[0].center
        self.player = Player(player_spawn[0], player_spawn[1], 
                             self.foreground, 
                             obstacles=[])
        
    def revive_player(self):
        """
        Show instructions and revive the player after dying.
        """
        self.instruction_text = RetryInstructionText(self.screen, (100, 100))
        self.player.dead = False

    def move_player_to_spawn(self):
        """
        Move the camera to the current spawn point.
        """
        self.player.rect.center = self.current_spawn
        self.camera.update(self.player.rect)
        self.fades['revive_fade_in'].start()
        
    def setup_triggers(self):
        """
        Setup the triggers for the scene.
        """
        self.init_trigger("death", lambda: self.fades['death_fade_out'].start(), triggered_once=False)
        self.init_trigger("end_of_phase", lambda: self.fades['fade_out'].start())

    def increment_spawn_index(self):
        """
        Increment the spawn index.
        """
        self.instruction_text.visible = True
        self.spawn_index += 1
        self.current_spawn = self.spawns_rects[self.spawn_index].center 
        
    def create_lampposts(self):
        """
        Create lampposts with associated ConeLight objects.
        Assign a unique blink offset to each lamppost.
        """
        self.lamppost_blink_timer = 0
        self.lamppost_blink_state = 1
        lamppost_positions = self.foreground.load_layer_entities("lampposts")
        for index, lamppost in enumerate(lamppost_positions.values()):
            light = ConeLight(
                (lamppost.x, lamppost.y),
                direction=(0, 1),
                angle=35,
                distance=260,
            )
            light.blink_offset = index * 2
            self.lampposts_group.add(light)
            self.lights_group.add(light)

    def update(self):
        dt = self.director.clock.get_time() / 1000
        
        # Update entities
        self.player.update(self.pressed_keys, dt)
            
        self.fireflies_group.update()
        
        self.lights_group.update()

        # Lamppost blink
        self.lamppost_blink_timer += dt
        for light in self.lampposts_group:
            adjusted_timer = (self.lamppost_blink_timer - light.blink_offset) % 6
            if 0 <= adjusted_timer < 1:  
                light.intensity = adjusted_timer
            elif 1 <= adjusted_timer < 3:  
                light.intensity = 1
            elif 3 <= adjusted_timer < 4:
                light.intensity = 1 - (adjusted_timer - 3)
            elif 4 <= adjusted_timer < 6:
                light.intensity = 0
        
        # Check player dying conditions
        for light in self.lights_group:          
            if light.intensity > 0.4 and self.player.check_pixel_perfect_collision(light) and not self.player.is_dying and not self.player.dead: 
                self.player.dying()
                self.fades['death_fade_out'].start()

        # Update triggers
        for trigger in self.triggers:
            trigger.check(self.player.rect)
            trigger.update(dt)

        # Update fades
        for fade in self.fades.values():
            fade.update(dt)

        self.instruction_text.update(dt)
        
        self.camera.update(self.player.rect)

    def draw(self):
        offset = self.camera.get_offset()

        self.background.draw(self.screen, offset)
        self.foreground.draw(self.screen, offset)
        self.player.draw(self.screen, camera_offset=offset)
        
        for firefly in self.fireflies_group:
            firefly.draw(self.screen, offset)
        
        for light in self.lampposts_group:
            light.draw(self.screen, offset)
        
        for trigger in self.triggers:
            trigger.draw(self.screen)

        self.instruction_text.draw(self.screen)

        for fade in self.fades.values():
            fade.draw()

    def continue_procedure(self):
        """
        Continue the procedure after the fade out.
        """
        self.sound_manager.play_sound("cemetery_background_sound.ogg", "assets\\sounds", category='ambient', loop=True)

    def end_of_phase(self, scene: str):
        """
        Action that ends the phase.
        """
        self.director.scene_manager.change_scene(scene)
