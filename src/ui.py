from action import Action
import os
import yaml

class UI:
    def display_status(self, character):
        print(f"\n==== {character.name} 的状态 ====")
        for key, value in character.state.items():
            print(f"{key}: {value}")

    def get_action_choice(self, player, partner):
        """获取玩家选择的行动"""
        #TODO: 从文件读取行动列表
        #TODO: 支持多个不冲突的行动
        #TODO: 更合理的可选行动布局
        with open('data/actions/index.yaml', 'r', encoding='utf-8') as file:
            actions_data = yaml.safe_load(file)
        actions = [Action(id, 'data/actions/'+file_name, player, partner) for id, file_name in actions_data.items()]
        
        print("\n可选行动:")
        j = 0
        map = [0] * len(actions)
        for i, action in enumerate(actions):
            if action.can_execute():
                print(f"{j + 1}. {action.name}")
                map[j] = i
                j += 1
        choice = int(input("选择行动 (输入编号): ")) - 1
        return actions[map[choice]]

    def display_result(self, result):
        print(f"\n{result}")

    # TODO: 从文件读取结局文本
    def display_end_message(self, player, partner):
        if partner.state["性欲"] >= 100:
            print(f"\n{partner.name} 已经完全沉醉于快感中，他的身体不受控制地抽搐起来，手指在你身上抓出一道道痕迹，用最缠绵的声音呻吟着达到了巅峰。" +\
                  "乳白色的液体从他的阴茎喷涌而出。\n\n过了许久，他才慢慢恢复了平静，脸上泛起一片红晕。" +\
                      "\n\n“我爱你。”他凑到你的耳边轻轻对你说，然后在你脸上亲了一下。\n\n")
        #print(f"你的历史操作:")
        #for action in player.getHistory():
        #    print(action)
    
    def clean_screen(self):
        os.system('cls||clear')

