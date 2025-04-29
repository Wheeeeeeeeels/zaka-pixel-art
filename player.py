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
        self.state = "idle"  # idle, running, jumping, falling, attacking
        self.animation_frame = 0
        self.animation_timer = 0
        self.on_ground = False
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 20  # 攻击动作持续帧数
        self.attack_cooldown = 30  # 攻击冷却帧数
        self.attack_damage = 10
        self.health = 100
        self.max_health = 100
        
        # 加载玩家精灵图
        self.sprite_sheet = pygame.image.load(config.PLAYER_SPRITE_PATH).convert_alpha()
        self.animations = {
            "idle": self.load_animation_frames(0, 4),
            "running": self.load_animation_frames(4, 8),
            "jumping": self.load_animation_frames(8, 9),
            "falling": self.load_animation_frames(9, 10),
            "attacking": self.load_animation_frames(10, 12)
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
        if not self.attacking:  # 攻击时不能移动
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
                if not self.jumping and not self.attacking:
                    self.state = "idle"
                    
        # 跳跃
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground and not self.attacking:
            self.velocity_y = -self.config.JUMP_FORCE
            self.jumping = True
            self.on_ground = False
            self.state = "jumping"
            
        # 攻击
        if keys[pygame.K_j] and not self.attacking and self.attack_timer <= 0:
            self.start_attack()
            
    def start_attack(self):
        self.attacking = True
        self.attack_timer = self.attack_duration
        self.state = "attacking"
        self.animation_frame = 0
        
    def update_attack(self):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
                self.attack_timer = self.attack_cooldown
                self.state = "idle"
        elif self.attack_timer > 0:
            self.attack_timer -= 1
            
    def get_attack_rect(self):
        if not self.attacking:
            return None
        
        attack_width = self.width
        attack_height = self.height
        
        if self.facing_right:
            return pygame.Rect(self.x + self.width, self.y,
                             attack_width, attack_height)
        else:
            return pygame.Rect(self.x - attack_width, self.y,
                             attack_width, attack_height)
            
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
        # 更新攻击状态
        self.update_attack()
        
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
        
        # 绘制生命值条
        health_width = 50
        health_height = 5
        health_x = screen_x + (self.width - health_width) // 2
        health_y = screen_y - 10
        
        # 背景
        pygame.draw.rect(screen, self.config.RED,
                        (health_x, health_y, health_width, health_height))
        # 当前生命值
        current_health_width = (self.health / self.max_health) * health_width
        pygame.draw.rect(screen, self.config.GREEN,
                        (health_x, health_y, current_health_width, health_height))
        
        # 调试：显示攻击范围
        if self.attacking and self.config.DEBUG:
            attack_rect = self.get_attack_rect()
            if attack_rect:
                pygame.draw.rect(screen, self.config.RED,
                               (attack_rect.x - camera.x,
                                attack_rect.y - camera.y,
                                attack_rect.width,
                                attack_rect.height), 1) 