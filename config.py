class Config:
    # 屏幕设置
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    
    # 玩家设置
    PLAYER_SPEED = 5
    JUMP_FORCE = 15
    GRAVITY = 0.8
    
    # 动画设置
    ANIMATION_SPEED = 5
    
    # 地图设置
    TILE_SIZE = 32
    MAP_WIDTH = 100 * TILE_SIZE  # 100个瓦片宽
    MAP_HEIGHT = 50 * TILE_SIZE  # 50个瓦片高
    
    # 颜色设置
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    # 资源路径
    PLAYER_SPRITE_PATH = "assets/images/characters/player.png"
    TILESET_PATH = "assets/images/tiles/tileset.png"
    MAP_DATA_PATH = "assets/data/maps.json"

    def __init__(self):
        # 屏幕设置
        self.SCREEN_WIDTH = self.SCREEN_WIDTH
        self.SCREEN_HEIGHT = self.SCREEN_HEIGHT
        self.FPS = self.FPS
        
        # 游戏设置
        self.TILE_SIZE = self.TILE_SIZE
        self.PLAYER_SPEED = self.PLAYER_SPEED
        self.GRAVITY = self.GRAVITY
        
        # 颜色设置
        self.BLACK = self.BLACK
        self.WHITE = self.WHITE
        self.RED = self.RED
        self.BLUE = self.BLUE
        self.GREEN = self.GREEN
        
        # 资源路径
        self.ASSETS_PATH = "assets/"
        self.IMAGES_PATH = self.ASSETS_PATH + "images/"
        self.SOUNDS_PATH = self.ASSETS_PATH + "sounds/"
        self.MAPS_PATH = self.ASSETS_PATH + "maps/" 