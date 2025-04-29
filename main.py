import pygame
import sys
from config import Config
from game_engine import GameEngine
from menu import Menu
from sound_manager import SoundManager

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    SETTINGS = "settings"

class AngelWar:
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        pygame.display.set_caption("Zaka Puzzle")
        self.clock = pygame.time.Clock()
        self.sound_manager = SoundManager(self.config)
        self.game_engine = GameEngine(self.config)
        self.menu = Menu(self.config, self.sound_manager)
        self.state = GameState.MENU
        self.running = True
        
        # 播放菜单音乐
        self.sound_manager.play_music('menu')
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.MENU
                        self.sound_manager.play_music('menu')
                    elif self.state == GameState.MENU:
                        self.running = False
                        
            elif self.state == GameState.MENU:
                action = self.menu.handle_input(event)
                if action == "start":
                    self.state = GameState.PLAYING
                    self.sound_manager.play_music('game')
                elif action == "settings":
                    self.state = GameState.SETTINGS
                elif action == "quit":
                    self.running = False
                    
    def update(self):
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            self.game_engine.player.handle_input(keys)
            self.game_engine.update()
        elif self.state == GameState.MENU:
            self.menu.update()
            
    def render(self):
        if self.state == GameState.PLAYING:
            self.game_engine.render(self.screen)
        elif self.state == GameState.MENU:
            self.menu.draw(self.screen)
            
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.config.FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = AngelWar()
    game.run() 