from action import Action
import os

class UI:
    def display_status(self, character):
        print(f"\n==== {character.name} 的状态 ====")
        for key, value in character.state.items():
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

    def display_end_message(self, player, partner):
        if partner.state["高潮"]:
            print(f"\n{partner.name} 已经完全沉醉于快感中，他的身体不受控制地抽搐起来，手指在你身上抓出一道道痕迹，用最缠绵的声音呻吟着达到了巅峰。" +\
                  "乳白色的液体从他的阴茎喷涌而出。过了许久，他才慢慢恢复了平静，脸上泛起一片红晕。" +\
                      "\n “我爱你。”他凑到你的耳边轻轻对你说，然后在你脸上亲了一下。")
            print(f"你的历史操作:")
            for action in player.getHistory():
                print(action)
    
    def clean_screen(self):
        os.system('cls||clear')

