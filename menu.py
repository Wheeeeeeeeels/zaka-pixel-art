import pygame

class MenuItem:
    def __init__(self, text, action, font, color, hover_color):
        self.text = text
        self.action = action
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.surface = self.font.render(
            self.text, True, 
            self.hover_color if self.is_hovered else self.color
        )
        
    def draw(self, screen, x, y):
        self.rect.center = (x, y)
        screen.blit(self.surface, self.rect)

class Menu:
    def __init__(self, config, sound_manager):
        self.config = config
        self.sound_manager = sound_manager
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 72)
        
        # 菜单项
        self.items = [
            MenuItem("开始游戏", "start", self.font, 
                    self.config.WHITE, self.config.GREEN),
            MenuItem("设置", "settings", self.font,
                    self.config.WHITE, self.config.GREEN),
            MenuItem("退出", "quit", self.font,
                    self.config.WHITE, self.config.GREEN)
        ]
        
        # 标题
        self.title = MenuItem("Zaka Puzzle", None, self.title_font,
                            self.config.WHITE, self.config.WHITE)
                            
        self.selected_item = None
        
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for item in self.items:
                if item.is_hovered:
                    self.sound_manager.play_sound('menu_select')
                    return item.action
        return None
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for item in self.items:
            item.update(mouse_pos)
            
    def draw(self, screen):
        # 绘制背景
        screen.fill(self.config.BLACK)
        
        # 绘制标题
        self.title.draw(screen, 
                       self.config.SCREEN_WIDTH // 2,
                       self.config.SCREEN_HEIGHT // 4)
        
        # 绘制菜单项
        start_y = self.config.SCREEN_HEIGHT // 2
        spacing = 60
        for i, item in enumerate(self.items):
            item.draw(screen,
                     self.config.SCREEN_WIDTH // 2,
                     start_y + i * spacing) 