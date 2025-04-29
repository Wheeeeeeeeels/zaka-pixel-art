import pygame

class Camera:
    def __init__(self, config):
        self.config = config
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.smooth_speed = 0.1
        
    def update(self, player):
        # 计算目标位置（玩家位置居中）
        self.target_x = player.x - self.config.SCREEN_WIDTH // 2
        self.target_y = player.y - self.config.SCREEN_HEIGHT // 2
        
        # 平滑移动相机
        self.x += (self.target_x - self.x) * self.smooth_speed
        self.y += (self.target_y - self.y) * self.smooth_speed
        
        # 限制相机范围（可选）
        self.x = max(0, min(self.x, self.config.MAP_WIDTH - self.config.SCREEN_WIDTH))
        self.y = max(0, min(self.y, self.config.MAP_HEIGHT - self.config.SCREEN_HEIGHT)) 