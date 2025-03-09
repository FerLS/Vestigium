import os
import random
import pygame
from resource_manager import ResourceManager

class SoundManager(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            pygame.mixer.pre_init(44100, -16, 2, 4096)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(8)
            cls._instance.channels = [pygame.mixer.Channel(i) for i in range(8)]
            cls._instance.music_volume = 0.5
            cls._instance.sound_volume = 0.5
            cls._instance.resource_manager = ResourceManager()
            cls._instance.footstep_channel = pygame.mixer.Channel(7)

        return cls._instance

    # Music related methods
    def play_music(self, music_name, music_path, loop=-1):
        fullname = os.path.join(music_path, music_name)
        pygame.mixer.music.load(fullname)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loop)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume)

    def get_music_volume(self):
        return pygame.mixer.music.get_volume()

    def play_sound(self, sound_name, sound_path, volume=None, pan=0.5):
        sound = ResourceManager().load_sound(sound_name, sound_path)
        if sound:
            """
            if "footstep" in sound_name.lower():
                if not self.footstep_channel.get_busy(): 
                    self.footstep_channel.set_volume(self.sound_volume)
                    self.footstep_channel.play(sound)
            else:"""
                # Para otros sonidos, buscar un canal libre
            canal_libre = pygame.mixer.find_channel()
            if canal_libre:
                final_volume = volume if volume is not None else self.sound_volume
                left = max(0.0, 1.0 - pan) * final_volume
                right = max(0.0, pan) * final_volume
                canal_libre.set_volume(left, right)
                canal_libre.play(sound)

    def stop_all_sounds(self):
        for channel in self.channels:
            channel.stop()

    def set_sound_volume(self, volume):
        self.sound_volume = max(0.0, min(1.0, volume))

    def get_sound_volume(self):
        return self.sound_volume
