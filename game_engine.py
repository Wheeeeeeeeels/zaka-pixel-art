import pygame
from player import Player
from map import Map
from camera import Camera

class GameEngine:
    def __init__(self, config):
        self.config = config
        self.map = Map(config)
        self.player = Player(config)
        self.camera = Camera(config)
        
    def update(self):
        self.player.update(self.map)
        self.map.update()
        self.camera.update(self.player)
        
    def render(self, screen):
        screen.fill(self.config.BLACK)
        self.map.render(screen, self.camera)
        self.player.render(screen, self.camera) 