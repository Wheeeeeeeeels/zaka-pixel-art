import pygame
import os

class SoundManager:
    def __init__(self, config):
        self.config = config
        pygame.mixer.init()
        self.sounds = {}
        self.music = {}
        self.load_sounds()
        
    def load_sounds(self):
        # 加载音效
        self.sounds = {
            'jump': pygame.mixer.Sound(os.path.join(self.config.SOUNDS_PATH, 'jump.wav')),
            'land': pygame.mixer.Sound(os.path.join(self.config.SOUNDS_PATH, 'land.wav')),
            'walk': pygame.mixer.Sound(os.path.join(self.config.SOUNDS_PATH, 'walk.wav')),
            'menu_select': pygame.mixer.Sound(os.path.join(self.config.SOUNDS_PATH, 'menu_select.wav'))
        }
        
        # 加载音乐
        self.music = {
            'menu': os.path.join(self.config.SOUNDS_PATH, 'menu.mp3'),
            'game': os.path.join(self.config.SOUNDS_PATH, 'game.mp3')
        }
        
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            
    def play_music(self, music_name, loop=True):
        if music_name in self.music:
            pygame.mixer.music.load(self.music[music_name])
            pygame.mixer.music.play(-1 if loop else 0)
            
    def stop_music(self):
        pygame.mixer.music.stop()
        
    def set_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)
        pygame.mixer.music.set_volume(volume) 