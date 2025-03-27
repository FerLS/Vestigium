import os
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
            pygame.mixer.set_reserved(4)
            cls._instance.channels = [pygame.mixer.Channel(i) for i in range(8)]

            # Grupos de canales por categoría
            cls._instance.channel_groups = {
                'player': [0, 1, 2],
                'ambient': [3],
                'enemies': [4]
            }

            cls._instance.music_volume = 0.5
            cls._instance.sound_volume = 0.5
            cls._instance.resource_manager = ResourceManager()

        return cls._instance

    # ==========================
    # MUSIC METHODS
    # ==========================
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

    # ==========================
    # SOUND METHODS
    # ==========================
    def play_sound(self, sound_name, sound_path, category='default', pan=0.5, loop=False):
        sound = self.resource_manager.load_sound(sound_name, sound_path)
        if not sound:
            return

        # Calcular volumen izquierdo y derecho usando pan
        left = max(0.0, min(1.0, 1.0 - pan)) * self.sound_volume
        right = max(0.0, min(1.0, pan)) * self.sound_volume

        # Buscar canal en el grupo
        group_channels = self.channel_groups.get(category, [])
        channel = None
        for ch_index in group_channels:
            ch = self.channels[ch_index]
            if not ch.get_busy():
                channel = ch
                break

        # Si no hay canal libre, usar uno no reservado
        if not channel:
            channel = pygame.mixer.find_channel()

        if channel:
            channel.set_volume(left, right)
            loops = -1 if loop else 0
            channel.play(sound, loops=loops)

    def stop_all_sounds(self):
        for channel in self.channels:
            channel.stop()

    def set_sound_volume(self, volume):
        self.sound_volume = max(0.0, min(1.0, volume))

    def get_sound_volume(self):
        return self.sound_volume
