# 导入外部标准模块
import sys
from time import sleep

import pygame

# 导入类
from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from music import Music


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        # 每当创建类的实例对象时,自动被调用
        """初始化游戏并创建游戏资源及属性"""
        pygame.init()
        # 创建Settings实例,并调用属性来创建屏幕
        self.settings = Settings()
        # 加载背景图片
        self.background_image = pygame.image.load("images/background.png")
        # 缩放背景图片以适应屏幕大小
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.settings.screen_width, self.settings.screen_height))
        # 创建表示背景的Rect对象
        self.background_rect = self.background_image.get_rect()
        # 初始时，背景图片的y坐标为0
        self.background_y = 0
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #创建音乐
        self.music = Music()  # 创建Music对象

        # 创建一个用于存储游戏统计信息的实例
        #并创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # 创建Ship实例
        self.ship = Ship(self)
        # 创建用于存储子弹的编组
        self.bullets = pygame.sprite.Group()
        # 创建Alien实例,使用一个存储外星人群的编组方法
        self.aliens = pygame.sprite.Group()
        # 调用接下来将编写的方法_create_fleet()
        self._create_fleet()
        # 创建play按钮
        self.play_button = Button(self, "Play")

        #创建一个Clock对象用于控制帧率
        self.clock = pygame.time.Clock()

    def run_game(self):
        self.music.play_background_music(-1)  # 循环播放背景音乐
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            # 每次循环时都重绘屏幕.
            self._update_screen()

    def _check_events(self):
        # 响应键盘和鼠标事件.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #退出前将最高分写入文件保存
                with open('high_score.txt', 'w') as file_object:
                    file_object.write(str(self.stats.high_score))
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键."""
        if event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            # 退出前将最高分写入文件保存
            with open('high_score.txt', 'w') as file_object:
                file_object.write(str(self.stats.high_score))
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            self.toggle_pause()


    def _check_keyup_events(self, event):
        """响应松开按键."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """玩家单击play按钮开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #重置游戏(速度设置)进度
            self._start_game()

    def _start_game(self):
        # 重置游戏动态设置并更新游戏统计信息.
        #设置
        self.settings.initialize_dynamic_settings()
        #统计
        self.stats.reset_stats()
        self.stats.game_active = True
        #更新信息图像
        self.sb.prep_images()
        # 清空余下的外星人和子弹
        self.aliens.empty()
        self.bullets.empty()
        # 创建一群新的外星人并热让飞船居中
        self._create_fleet()
        self.ship.center_ship()
        # 隐藏鼠标光标.
        pygame.mouse.set_visible(False)

    def toggle_pause(self):
        self.stats.game_active = not self.stats.game_active
        if not self.stats.game_active:
            pygame.mixer.pause()  # 暂停背景音乐
        else:
            pygame.mixer.unpause()  # 恢复背景音乐

    def _fire_bullet(self):
        """创建新子弹,并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置,并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 检查是否有子弹击中外星人,如果是,则删除相应的子弹和外星人.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # 删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()
            #整群外星人被消灭后,加快游戏节奏
            self.settings.increase_speed()
            #提高等级
            self.start_new_level()
        #积分
        if collisions:
            for _ in collisions.values():
                self.stats.score += self.settings.alien_points
                self.sb.prep_score()
                self.sb.check_high_score()
                self.music.play_shoot_sound()

    def start_new_level(self):
        """更新等级信息"""
        self.stats.level += 1
        self.sb.prep_level()

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘并更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检测外星人是否到达屏幕底部
        self._check_aliens_bottom()

    def _create_fleet(self):
        """创建外星人群."""
        # 创建一个外星人并计算一行可容纳多少个外星人.
        # 设置屏幕两边间距,外星人间距为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            # 创建第一行外星人.
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # 创建一个外星人并将其加入当前行
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien.rect.height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移,并改变它们的方向."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            """响应飞船被外星人撞到"""
            # 将ships_left减1并更新计数牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人,并重置飞船位置为屏幕底部中央.
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 按照飞船被撞到处理
                self._ship_hit()
                break

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 让背景图滚动
        self.background_y += 1
        if self.background_y >= self.settings.screen_height:
            self.background_y = 0

        # 绘制背景图
        self.screen.blit(self.background_image, (0, self.background_y))
        self.screen.blit(self.background_image, (0, self.background_y - self.settings.screen_height))

        # 绘制飞船
        self.ship.blitme()

        # 绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # 绘制外星人
        self.aliens.draw(self.screen)

        # 绘制得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 控制帧率
        self.clock.tick(60)  # 这里的60表示帧率上限为60fps

        # 让最近绘制的屏幕可见
        pygame.display.flip()



if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai_game = AlienInvasion()
    ai_game.run_game()
