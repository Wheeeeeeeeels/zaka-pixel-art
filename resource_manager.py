import pygame
import json
import os

class ResourceManager:
    def __init__(self, config):
        self.config = config
        self.images = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}
        self.data = {}
        
    def load_image(self, name, path):
        """加载图像资源"""
        try:
            image = pygame.image.load(os.path.join(self.config.IMAGES_PATH, path))
            self.images[name] = image
            return image
        except Exception as e:
            print(f"Error loading image {name}: {e}")
            return None
            
    def load_sound(self, name, path):
        """加载音效资源"""
        try:
            sound = pygame.mixer.Sound(os.path.join(self.config.SOUNDS_PATH, path))
            self.sounds[name] = sound
            return sound
        except Exception as e:
            print(f"Error loading sound {name}: {e}")
            return None
            
    def load_music(self, name, path):
        """加载音乐资源"""
        try:
            self.music[name] = os.path.join(self.config.SOUNDS_PATH, path)
            return self.music[name]
        except Exception as e:
            print(f"Error loading music {name}: {e}")
            return None
            
    def load_font(self, name, path, size):
        """加载字体资源"""
        try:
            font = pygame.font.Font(os.path.join(self.config.ASSETS_PATH, path), size)
            self.fonts[name] = font
            return font
        except Exception as e:
            print(f"Error loading font {name}: {e}")
            return None
            
    def load_data(self, name, path):
        """加载数据资源"""
        try:
            with open(os.path.join(self.config.ASSETS_PATH, path), 'r', encoding='utf-8') as f:
                self.data[name] = json.load(f)
            return self.data[name]
        except Exception as e:
            print(f"Error loading data {name}: {e}")
            return None
            
    def get_image(self, name):
        """获取图像资源"""
        return self.images.get(name)
        
    def get_sound(self, name):
        """获取音效资源"""
        return self.sounds.get(name)
        
    def get_music(self, name):
        """获取音乐资源"""
        return self.music.get(name)
        
    def get_font(self, name):
        """获取字体资源"""
        return self.fonts.get(name)
        
    def get_data(self, name):
        """获取数据资源"""
        return self.data.get(name) 