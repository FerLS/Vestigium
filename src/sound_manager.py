import os
import pygame

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


    # Sound related methods

