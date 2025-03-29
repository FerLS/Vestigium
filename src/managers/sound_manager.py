import os
import pygame
from managers.resource_manager import ResourceManager

class SoundManager:
    """
    Singleton class for managing all music and sound effects in the game.
    Handles initialization, playback, volume control, and categorized channel usage.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Mixer configuration for optimal latency and quality
            pygame.mixer.pre_init(44100, -16, 2, 4096)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(8)
            pygame.mixer.set_reserved(4)  # Reserve first 4 channels (e.g., for priority sounds)

            # Create and store dedicated channels
            cls._instance.channels = [pygame.mixer.Channel(i) for i in range(8)]

            # Logical grouping of channels for sound categories
            cls._instance.channel_groups = {
                'player': [0, 1, 2],
                'ambient': [3],
                'enemies': [4]
            }

            cls._instance.music_volume = 0.5
            cls._instance.sound_volume = 0.5
            cls._instance.resource_manager = ResourceManager()

        return cls._instance

    def play_music(self, 
                   music_name: str, 
                   music_path: str, 
                   loop: int = -1):
        """
        Loads and plays a music track from disk. Supports looping.

        :param music_name: Name of the music file (e.g., "track.mp3").
        :param music_path: Path to the directory containing the music file.
        :param loop: Number of times to loop the music (-1 for infinite loop).
        """
        fullname = os.path.join(music_path, music_name)
        pygame.mixer.music.load(fullname)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loop)

    def stop_music(self):
        """
        Stops any currently playing music immediately.
        """
        pygame.mixer.music.stop()

    def pause_music(self):
        """
        Pauses the current music playback.
        """
        pygame.mixer.music.pause()

    def resume_music(self):
        """
        Resumes the paused music.
        """
        pygame.mixer.music.unpause()

    def set_music_volume(self, 
                         volume: float):
        """
        Sets the global music volume (range: 0.0 to 1.0).

        :param volume: Volume level between 0.0 (mute) and 1.0 (max).
        """
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume)

    def get_music_volume(self) -> float:
        """
        Returns the current music volume level.
        """
        return pygame.mixer.music.get_volume()

    def play_sound(
        self,
        sound_name: str,
        sound_path: str,
        category: str = 'default',
        pan: float = 0.5,
        loop: bool = False
    ):
        """
        Plays a sound effect with optional stereo panning and loop control.

        :param sound_name: Name of the sound file (e.g., "effect.wav").
        :param sound_path: Path to the directory containing the sound file.
        :param category: Category of the sound (e.g., 'player', 'ambient').
        :param pan: Stereo panning value (0.0 = left, 1.0 = right).
        :param loop: Whether to loop the sound (True for infinite loop).
        """
        sound = self.resource_manager.load_sound(sound_name, sound_path)
        if not sound:
            return

        # Compute stereo volume based on pan
        left = max(0.0, min(1.0, 1.0 - pan)) * self.sound_volume
        right = max(0.0, min(1.0, pan)) * self.sound_volume

        # Try to get a free channel in the category group
        group_channels = self.channel_groups.get(category, [])
        channel = None
        for ch_index in group_channels:
            ch = self.channels[ch_index]
            if not ch.get_busy():
                channel = ch
                break

        # Fallback: use any free unreserved channel
        if not channel:
            channel = pygame.mixer.find_channel()

        if channel:
            channel.set_volume(left, right)
            loops = -1 if loop else 0
            channel.play(sound, loops=loops)

    def stop_all_sounds(self):
        """
        Stops all currently playing sounds on all channels.
        """
        for channel in self.channels:
            channel.stop()

    def set_sound_volume(self,
                        volume: float):
        """
        Sets the global volume for sound effects (range: 0.0 to 1.0).

        :param volume: Volume level between 0.0 (mute) and 1.0 (max).
        """
        self.sound_volume = max(0.0, min(1.0, volume))

    def get_sound_volume(self) -> float:
        """
        Returns the current sound effect volume level.
        """
        return self.sound_volume
