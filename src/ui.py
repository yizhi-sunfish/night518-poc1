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
        # TODO：目前先手动加入脱衣选项，之后再想怎么更好地实现
        actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner,'右手',None,'白色背心'))
        actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner,'左手',None,'四角内裤'))
        
        print("\n可选行动:")
        j = 0
        map = [0] * len(actions)
        for i, action in enumerate(actions):
            if action.can_execute():
                print(f"{j + 1}. {action.name.format(chosenCloth="衣物")}")
                map[j] = i
                j += 1
        choice = int(input("选择行动 (输入编号): ")) - 1
        return actions[map[choice]]
    """
    def get_multiple_actions(self, player, partner):
        
        with open('data/actions/index.yaml', 'r', encoding='utf-8') as file:
            actions_data = yaml.safe_load(file)
        actions = [Action(id, 'data/actions/' + file_name, player, partner) for id, file_name in actions_data.items()]
        
        # 额外加入脱衣选项
        actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, '右手', None, '白色背心'))
        actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, '左手', None, '四角内裤'))
        
        # 获取玩家所有可用的身体部位
        available_body_parts = player.bodyParts  # 假设返回的是 {"嘴": True, "左手": True, "右手": False}
        
        # 存储按身体部位分类的可执行动作
        available_actions = {}
        action_index_map = []
        j = 0  # 仅计算可执行的选项编号
        
        # 遍历所有行动，将它们按 actBodyPart 分类
        for i, action in enumerate(actions):
            if not action.can_execute():
                continue  # 过滤不可执行的动作

            # 获取该 action 可以在哪些部位执行（可能是单个字符串或列表）
            possible_parts = action.possibleBodyPart if isinstance(action.possibleBodyPart, list) else [action.possibleBodyPart]

            # 选择一个可用的身体部位
            chosen_part = None
            for part in possible_parts:
                if part in partner.bodyParts:  # 确保该部位可用
                    chosen_part = part
                    break
            
            if not chosen_part:  # 如果没有找到合适的部位，跳过
                continue

            # 分类存储可用动作
            if chosen_part not in available_actions:
                available_actions[chosen_part] = []
            available_actions[chosen_part].append((j + 1, action))
            action_index_map.append((j + 1, action, chosen_part))  # 记录编号、动作、身体部位
            j += 1

        # 显示可选行动
        print("\n可选行动:")
        for body_part, actions_list in available_actions.items():
            action_texts = [f"{num}. {action.name.format(chosenCloth='衣物')}" for num, action in actions_list]
            print(f"【{body_part}】 " + "  ".join(action_texts))

        # 让玩家输入多个编号
        choices = input("\n选择多个行动（用空格分隔编号，例如：1 3 5）: ").split()
        
        # 解析选择
        selected_actions = []
        occupied_parts = set()  # 记录已使用的身体部位，防止冲突
        for choice in choices:
            try:
                choice = int(choice)
                action, chosen_part = next((a, p) for num, a, p in action_index_map if num == choice)

                # 检查身体部位冲突
                if chosen_part in occupied_parts:
                    print(f"⚠️ 冲突: {chosen_part} 已经在执行其他行动，跳过 {action.name}")
                    continue

                selected_actions.append(action)
                occupied_parts.add(chosen_part)  # 标记已使用的身体部位
                
            except (ValueError, StopIteration):
                print(f"⚠️ 无效选择: {choice}，跳过")

        return selected_actions  # 返回选定的多个动作
    """
    """
    def get_multiple_actions(self, player, partner):
        
        with open('data/actions/index.yaml', 'r', encoding='utf-8') as file:
            actions_data = yaml.safe_load(file)
        
        actions = []

        # 获取玩家所有可用的身体部位
        available_body_parts = player.bodyParts  # 例如 {"嘴": True, "左手": True, "右手": False}

        # 按身体部位存储可执行的动作
        available_actions = {part: [] for part in available_body_parts if available_body_parts[part]}
        
        # 遍历所有动作，为每个部位挑选可执行的 Action
        for id, file_name in actions_data.items():
            action_data = yaml.safe_load(open('data/actions/' + file_name, 'r', encoding='utf-8'))[id]
            possible_parts = action_data.get("possibleBodyPart", [])  # 可能是字符串或列表
            
            if isinstance(possible_parts, str):
                possible_parts = [possible_parts]  # 统一转换为列表

            for part in possible_parts:
                if part in available_actions:  # 该部位可用
                    action = Action(id, 'data/actions/' + file_name, player, partner, part)  # 设定 chosenPart
                    available_actions[part].append(action)

        # 额外加入脱衣选项（遍历所有可用部位，给它们加脱衣选项）
        #for body_part in available_actions.keys():
        #    actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, body_part, None, '衣物'))

        # 记录玩家最终选择的动作
        selected_actions = []

        # 逐个部位让玩家选择
        for body_part, actions_list in available_actions.items():
            if not actions_list:  # 该部位没有可执行的动作
                continue

            print(f"\n【{body_part}】可执行的行动:")
            for i, action in enumerate(actions_list, start=1):
                print(f"{i}. {action.name.format(chosenCloth='衣物')}")

            # 获取玩家输入
            while True:
                choice = input(f"选择 {body_part} 的行动 (输入编号, 0 跳过): ").strip()
                if choice.isdigit():
                    choice = int(choice)
                    if 0 <= choice <= len(actions_list):
                        break
                print("⚠️ 请输入正确的编号！")

            if choice > 0:
                selected_actions.append(actions_list[choice - 1])  # 记录玩家的选择

        return selected_actions  # 返回最终选择的所有动作
    """

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

