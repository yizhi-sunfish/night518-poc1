from character import Character
from event import Event
from ui import UI
import time

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
        self.running = True
        self.result = ""

    def play_turn(self):
        """处理游戏的一个回合"""
        '''
        print("Aaron:")
        print(self.player)
        print(self.player.bodyParts)
        print(self.player.clothing)
        print("Zayn:")
        print(self.partner)
        print(self.partner.bodyParts)
        print(self.partner.clothing)
        '''
        self.ui.clean_screen()
        self.ui.display_status(self.player, self.partner)
        time.sleep(0.5)
        self.ui.typewriter_panel(self.result)
        Event.check_triggers(self.player, self.partner,self.ui)
        time.sleep(0.5)
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
        if self.partner.state["性欲"] >= 100:
            self.running = False
    def run(self):
        """主循环"""
        while self.running:
            self.play_turn()
        self.ui.display_end_message(self.player, self.partner)

