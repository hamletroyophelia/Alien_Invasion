import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.score_rect = None
        self.score_image = None
        self.high_score_rect = None
        self.high_score_image = None
        self.level_image = None
        self.level_rect = None
        self.ships = None
        # 显示得分信息时使用的字体设置
        self.text_color = (110, 235, 110)
        self.font = pygame.font.SysFont(None, 40)
        # 准备初始当前得分,最高得分和等级图像
        self.prep_images()

    def prep_images(self):
        """绘制游戏数据图像信息"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转化为一幅渲染的图像"""
        rounded_score = round(self.stats.score, -1)
        score_str = 'score:' + '{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转化为一幅渲染的图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = 'max:' + '{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕顶部中央显示得分
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为渲染的图像"""
        level_str = 'level:' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        #把等级放在得分下面
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示余下的飞船数"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            #用生命值图片替换原来的飞船图片
            new_ship_image = pygame.image.load('images/heart.bmp')
            ship = Ship(self.ai_game)
            ship.image = new_ship_image
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示数据信息:得分,等级,生命"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
