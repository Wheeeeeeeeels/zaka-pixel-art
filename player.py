import pygame
import math

class Player:
    def __init__(self, config):
        self.config = config
        self.x = 100
        self.y = 100
        self.width = 32
        self.height = 48
        self.velocity_x = 0
        self.velocity_y = 0
        self.jumping = False
        self.facing_right = True
        self.state = "idle"  # idle, running, jumping, falling
        self.animation_frame = 0
        self.animation_timer = 0
        self.on_ground = False
        
        # 加载玩家精灵图
        self.sprite_sheet = pygame.image.load(config.PLAYER_SPRITE_PATH).convert_alpha()
        self.animations = {
            "idle": self.load_animation_frames(0, 4),
            "running": self.load_animation_frames(4, 8),
            "jumping": self.load_animation_frames(8, 9),
            "falling": self.load_animation_frames(9, 10)
        }
        
    def load_animation_frames(self, start_frame, end_frame):
        frames = []
        for i in range(start_frame, end_frame):
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * self.width, 0, self.width, self.height))
            frames.append(frame)
        return frames
        
    def handle_input(self, keys):
        # 水平移动
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.config.PLAYER_SPEED
            self.facing_right = False
            self.state = "running"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.config.PLAYER_SPEED
            self.facing_right = True
            self.state = "running"
        else:
            self.velocity_x = 0
            if not self.jumping:
                self.state = "idle"
                
        # 跳跃
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity_y = -self.config.JUMP_FORCE
            self.jumping = True
            self.on_ground = False
            self.state = "jumping"
            
    def check_collision(self, map):
        # 检查水平碰撞
        next_x = self.x + self.velocity_x
        tile_x = int(next_x // self.config.TILE_SIZE)
        tile_y_top = int(self.y // self.config.TILE_SIZE)
        tile_y_bottom = int((self.y + self.height) // self.config.TILE_SIZE)
        
        if map.is_collision(tile_x, tile_y_top) or map.is_collision(tile_x, tile_y_bottom):
            self.velocity_x = 0
            
        # 检查垂直碰撞
        next_y = self.y + self.velocity_y
        tile_y = int(next_y // self.config.TILE_SIZE)
        tile_x_left = int(self.x // self.config.TILE_SIZE)
        tile_x_right = int((self.x + self.width) // self.config.TILE_SIZE)
        
        if self.velocity_y > 0:  # 下落
            if map.is_collision(tile_x_left, tile_y) or map.is_collision(tile_x_right, tile_y):
                self.velocity_y = 0
                self.y = tile_y * self.config.TILE_SIZE - self.height
                self.jumping = False
                self.on_ground = True
                if self.state == "jumping":
                    self.state = "idle"
        elif self.velocity_y < 0:  # 上升
            if map.is_collision(tile_x_left, tile_y) or map.is_collision(tile_x_right, tile_y):
                self.velocity_y = 0
                self.y = (tile_y + 1) * self.config.TILE_SIZE
                
    def update(self, map):
        # 应用重力
        self.velocity_y += self.config.GRAVITY
        
        # 检查碰撞
        self.check_collision(map)
        
        # 更新位置
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # 更新动画
        self.animation_timer += 1
        if self.animation_timer >= self.config.ANIMATION_SPEED:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.animations[self.state])
            
    def render(self, screen, camera):
        # 获取当前动画帧
        current_frame = self.animations[self.state][self.animation_frame]
        
        # 根据朝向翻转图像
        if not self.facing_right:
            current_frame = pygame.transform.flip(current_frame, True, False)
            
        # 计算屏幕上的位置
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        
        # 绘制玩家
        screen.blit(current_frame, (screen_x, screen_y)) 