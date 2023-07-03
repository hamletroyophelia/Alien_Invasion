class GameStats:
    """跟踪游戏的统计信息."""

    def __init__(self, ai_game):
        """初始化统计信息."""
        self.score = None
        self.high_score = 0
        self.level = None
        self.ships_left = None
        self.settings = ai_game.settings
        self.reset_stats()

        #游戏刚启动处于活跃状态
        self.game_active = False

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息."""
        #飞船生命值
        self.ships_left = self.settings.ship_limit
        #积分和等级
        self.score = 0
        self.level = 1
