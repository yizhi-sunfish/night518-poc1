from character import Character
from event import Event
from ui import UI
import time
import plots

class Game:
    def __init__(self):
        """
        初始化游戏，包括玩家和伙伴角色、用户界面和游戏状态。\n
        属性:\n
            player (Character): 从 YAML 文件加载的主玩家角色。\n
            partner (Character): 从 YAML 文件加载的伙伴角色。\n
            ui (UI): 游戏的用户界面。\n
            running (bool): 一个标志，指示主游戏机制是否正在运行。\n
            result (str): 用于存储游戏结果的字符串。
        """
        
        self.player = Character("data/characters/player.yaml", is_player=True) 
        self.partner = Character("data/characters/partner.yaml", is_player=False)
        self.ui = UI()
        self.running = False
        self.result = "这个破旧的房间逼仄又安静。你爬到佐音身上，望向他，他的眼神和你对视，却又马上躲闪开。\n你们真的太久没见了，距离让他对亲热行为有些抗拒。不过，能顺利活着回来已经是很好的结果了，你不难想象是什么导致了他现在如此拘谨。\n但很显然，他的心还属于你，因为他一言不发地牵住了你的手，脸色已经微微发红。\n现在你们只需要慢慢来。"

    def play_turn(self):
        """处理游戏的一个回合"""
        self.ui.clean_screen()
        self.ui.display_status(self.player, self.partner)
        time.sleep(1)
        self.ui.typewriter_panel(self.result)
        time.sleep(1)
        Event.check_triggers(self.player, self.partner,self.ui)
        self.ui.console.print("")
        time.sleep(1)
        actions = self.ui.get_multiple_actions(self.player, self.partner)
        self.result = ""
        last_action = actions[-1]
        for action in actions:
            result = action.execute()
            if result is not None:
                self.result += result
                if action != last_action:
                    self.result += '\n\n'
            self.player.updateHistory(action)
        # 终止条件
        if self.partner.state["性欲"] >= 100 and self.partner.state["体感"] >= 100:
            self.running = False
    def run(self):
        self.ui.clean_screen()
        self.ui.display_title("May 18th (PoC)")
        plots.opening(self.ui,self.player,self.partner)
        self.running = True
        """主循环"""
        while self.running:
            self.play_turn()
        plots.ending(self.ui,self.player,self.partner)
        self.ui.display_end_message(self.player, self.partner)

