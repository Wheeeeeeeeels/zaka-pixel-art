import pygame
import sys
from config import Config
from game_engine import GameEngine

class AngelWar:
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        pygame.display.set_caption("Angel War")
        self.clock = pygame.time.Clock()
        self.game_engine = GameEngine(self.config)
        self.running = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def update(self):
        # 处理玩家输入
        keys = pygame.key.get_pressed()
        self.game_engine.player.handle_input(keys)
        
        # 更新游戏状态
        self.game_engine.update()
        
    def render(self):
        self.game_engine.render(self.screen)
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