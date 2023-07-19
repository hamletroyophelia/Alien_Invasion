import pygame


class Music:
    def __init__(self):
        pygame.mixer.init()
        self.shoot_sound = pygame.mixer.Sound("music/shoot.mp3")  # 替换为你的音效文件路径
        self.background_music = pygame.mixer.Sound(
            "music/Search music on Free Music Archive - Free Music Archive.mp3")  # 替换为你的背景音乐文件路径

    def play_shoot_sound(self):
        self.shoot_sound.play()

    def play_background_music(self, loops=-1):
        self.background_music.play(loops)
