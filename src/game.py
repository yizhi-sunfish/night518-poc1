from character import Character
from event import Event
from ui import UI

class Game:
    def __init__(self):
        self.player = Character("data/characters/player.yaml", is_player=True) 
        self.partner = Character("data/characters/partner.yaml", is_player=False)
        self.ui = UI()
        self.running = True
        self.result = ""

    def play_turn(self):
        """处理游戏的一个回合"""
        self.ui.clean_screen()
        self.ui.display_result(self.result)
        Event.check_triggers(self.partner)
        self.ui.display_status(self.partner)
        self.result = ""
        action = self.ui.get_action_choice(self.player, self.partner)
        self.result = action.execute()
        self.player.updateHistory(action)
        #actions = self.ui.get_multiple_actions(self.player, self.partner)
        #for action in actions:
        #    self.result += action.execute()
        #    self.result += '\n'
        
        # 终止条件
        if self.partner.state["性欲"] >= 100:
            self.running = False

    def run(self):
        """主循环"""
        while self.running:
            self.play_turn()
        self.ui.display_end_message(self.player, self.partner)

