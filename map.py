import pygame
import json

class Map:
    def __init__(self, config):
        self.config = config
        self.tile_size = 32
        self.tiles = []
        self.collision_map = []
        
        # 加载地图数据
        with open(config.MAP_DATA_PATH, 'r') as f:
            map_data = json.load(f)
            self.width = map_data['width']
            self.height = map_data['height']
            self.tiles = map_data['tiles']
            self.collision_map = map_data['collision']
            
        # 加载瓦片集
        self.tileset = pygame.image.load(config.TILESET_PATH).convert_alpha()
        
    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return 0
        
    def is_collision(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.collision_map[y][x] == 1
        return True
        
    def update(self):
        # 可以在这里添加地图更新逻辑
        pass
        
    def render(self, screen, camera):
        # 计算可见区域
        start_x = max(0, int(camera.x // self.tile_size))
        end_x = min(self.width, int((camera.x + self.config.SCREEN_WIDTH) // self.tile_size) + 1)
        start_y = max(0, int(camera.y // self.tile_size))
        end_y = min(self.height, int((camera.y + self.config.SCREEN_HEIGHT) // self.tile_size) + 1)
        
        # 渲染可见的瓦片
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_id = self.get_tile(x, y)
                if tile_id > 0:
                    # 计算瓦片在瓦片集中的位置
                    tile_x = (tile_id - 1) % (self.tileset.get_width() // self.tile_size)
                    tile_y = (tile_id - 1) // (self.tileset.get_width() // self.tile_size)
                    
                    # 计算屏幕上的位置
                    screen_x = x * self.tile_size - camera.x
                    screen_y = y * self.tile_size - camera.y
                    
                    # 绘制瓦片
                    screen.blit(self.tileset, 
                              (screen_x, screen_y),
                              (tile_x * self.tile_size, tile_y * self.tile_size,
                               self.tile_size, self.tile_size)) 