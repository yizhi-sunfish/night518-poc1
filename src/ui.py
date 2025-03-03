from action import Action
import os

class UI:
    def display_status(self, player, partner):
        print(f"\n==== {partner.name} 的状态 ====")
        for key, value in partner.state.items():
            print(f"{key}: {value}")

    def get_action_choice(self):
        """获取玩家选择的行动"""
        actions = [
            Action("轻吻", {"性欲": +2, "舒适度": +2}),
            Action("深入亲吻", {"性欲": +10, "舒适度": -5}, condition=lambda p, n: n.state["性欲"] > 10),
            Action("抚摸", {"舒适度": +2}),
            Action("拉开衣物", {"性欲": +5}, condition=lambda p, n: n.state["开放"] > 20),
            Action("脱掉衣物", {"性欲": +10}, condition=lambda p, n: n.state["开放"] > 30),
            Action("插入", {"性欲": +20, "舒适度": -30}, condition=lambda p, n: n.state["开放"] > 50),
            Action("抽插", {"性欲": +20, "舒适度": +30}, condition=lambda p, n: n.state["开放"] > 50)
        ]
        
        print("\n可选行动:")
        for i, action in enumerate(actions):
            print(f"{i + 1}. {action.name}")
        
        choice = int(input("选择行动 (输入编号): ")) - 1
        return actions[choice]

    def display_result(self, result):
        print(f"\n{result}")

    def display_end_message(self, partner):
        if partner.state["高潮"]:
            print(f"\n{partner.name} 达到了高潮，游戏结束。")
    
    def clean_screen(self):
        os.system('cls||clear')

