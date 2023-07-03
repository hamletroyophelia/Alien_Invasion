class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        #屏幕设置,大小和背景色
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (235, 235, 235)
        #飞船设置
        self.ship_limit = 3
        self.ship_speed = None
        #子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.bullet_speed = None
        #外星人设置
        self.fleet_drop_speed = 8
        self.alien_speed = None
        self.fleet_direction = None
        #加快游戏的节奏
        self.speedup_scale = 1.1
        #游戏奖励机制
        self.alien_points = None
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行变化的动态设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.8

        #fleet_direction为1表示向右,为-1表示向左
        self.fleet_direction = 1

        #记分
        self.alien_points = 50

    def increase_speed(self):
        #增加速度和分数奖励加快游戏进度
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        #增加子弹数,升级飞船
        self.bullets_allowed += 1
        #提高分数
        self.alien_points = int(self.alien_points * self.speedup_scale)
