from action import Action
import os

class UI:
    def display_status(self, character):
        print(f"\n==== {character.name} 的状态 ====")
        for key, value in character.state.items():
            print(f"{key}: {value}")

    def get_action_choice(self, player, partner):
        """获取玩家选择的行动"""
        #TODO: 从文件读取行动列表
        actions = [
            Action("表达爱意", {"开放": +5}),
            Action("责骂", {"开放": -5, "性欲": -5}),
            Action("轻吻", {"性欲": +2, "体感": +2, "开放": +2}),
            Action("深入亲吻", {"性欲": +5, "体感": 5, "开放": +5}, condition=lambda p, n: n.state["性欲"] > 10),
            Action("温柔爱抚", {"体感": +2, "开放": +2}),
            Action("拉开衣物", {"性欲": +5, "开放": +5}, condition=lambda p, n: n.state["开放"] > 20),
            Action("脱掉衣物", {"性欲": +5, "体感": +5, "开放": +5}, condition=lambda p, n: n.state["开放"] > 30),
            Action("舔舐乳头", {"性欲": +7, "体感": +7}, condition=lambda p, n: n.state["开放"] > 50),
            Action("粗暴地刺激性器官", {"性欲": +10, "体感": -10, "开放": +15}, condition=lambda p, n: n.state["开放"] > 50),
            Action("互相口交", {"性欲": +20, "体感": +20, "开放": +20}, condition=lambda p, n: n.state["开放"] > 90),
            Action("插入", {"性欲": +20, "体感": -30}, condition=lambda p, n: n.state["开放"] > 60),
            Action("抽插", {"性欲": +20, "体感": +30}, condition=lambda p, n: n.state["开放"] > 60)
        ]
        
        print("\n可选行动:")
        j = 0
        map = [0] * len(actions)
        for i, action in enumerate(actions):
            if action.can_execute(player, partner):
                print(f"{j + 1}. {action.name}")
                map[j] = i
                j += 1
        choice = int(input("选择行动 (输入编号): ")) - 1
        return actions[map[choice]]

    def display_result(self, result):
        print(f"\n{result}")

    def display_end_message(self, player, partner):
        if partner.state["高潮"]:
            print(f"\n{partner.name} 已经完全沉醉于快感中，他的身体不受控制地抽搐起来，手指在你身上抓出一道道痕迹，用最缠绵的声音呻吟着达到了巅峰。" +\
                  "乳白色的液体从他的阴茎喷涌而出。\n\n过了许久，他才慢慢恢复了平静，脸上泛起一片红晕。" +\
                      "\n\n“我爱你。”他凑到你的耳边轻轻对你说，然后在你脸上亲了一下。\n\n")
#        print(f"你的历史操作:")
#        for action in player.getHistory():
#            print(action)
    
    def clean_screen(self):
        os.system('cls||clear')

