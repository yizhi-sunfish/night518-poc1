from action import Action
import os
import yaml
import copy

class UI:
    def display_status(self, character):
        print(f"\n==== {character.name} 的状态 ====")
        for key, value in character.state.items():
            print(f"{key}: {value}")
    def get_init_action_list(self, player, partner):

        with open('data/actions/index.yaml', 'r', encoding='utf-8') as file:
            self.actions_index_data = yaml.safe_load(file)
        self.init_actions = [Action(id, 'data/actions/' + file_name, player, partner, 'start') for id, file_name in self.actions_index_data.items()]
        
        # 额外加入脱衣选项
        self.init_actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, 'start', '右手', None, '白色背心'))
        self.init_actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, 'start', '左手', None, '四角内裤'))

    # deprecated
    def get_single_choice(self, player, partner):
        """获取玩家选择的行动"""
        with open('data/actions/index.yaml', 'r', encoding='utf-8') as file:
            self.actions_index_data = yaml.safe_load(file)
        actions = [Action(id, 'data/actions/'+file_name, player, partner, 'start') for id, file_name in self.actions_index_data.items()]
        # TODO：目前先手动加入脱衣选项，之后再想怎么更好地实现
        actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, 'start', '右手',None,'白色背心'))
        actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, 'start', '左手',None,'四角内裤'))
        
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
    
    def get_multiple_actions(self, player, partner):
        if not hasattr(self,'init_action_list'):
            self.get_init_action_list(player, partner)
        # 存储按身体部位分类的可执行动作
        available_actions = {}
        action_index_map = []
        j = 0  # 仅计算可执行的选项编号

        # 遍历玩家可用的身体部位
        # 在每个loop，查询当前身体部位是否被占用，如是，加入停止动作
        # 如否，查询当前部位可用动作
        for part in player.bodyParts:
            if part not in available_actions:
                available_actions[part] = []
            if player.bodyParts[part]['isOccupied']:
                # 加入继续和停止的动作
                path = {id:path for id, path in self.actions_index_data.items() if id == player.bodyParts[part]['currentAction']}
                continue_action = Action(player.bodyParts[part]['currentAction'], 'data/actions/' + path[player.bodyParts[part]['currentAction']],player,partner,'continue')
                end_action = Action(player.bodyParts[part]['currentAction'], 'data/actions/' + path[player.bodyParts[part]['currentAction']],player,partner,'end') 
                continue_action.name = "继续" + continue_action.name
                end_action.name = "停止" + end_action.name
                available_actions[part].append((j + 1, continue_action))
                action_index_map.append((j + 1, continue_action, part))
                available_actions[part].append((j + 2, end_action))
                action_index_map.append((j + 2, end_action, part))
                j += 2
            else:
                for i, action in enumerate(self.init_actions):
                    # 过滤不可执行的动作
                    if not action.can_execute():
                        continue  
                    possible_parts = action.possibleBodyParts if isinstance(action.possibleBodyParts, list) else [action.possibleBodyParts]
                    if part not in possible_parts:
                        continue

                    # 处理可执行的动作
                    if part not in available_actions:
                        available_actions[part] = []
                    action_copy = copy.deepcopy(action)
                    action_copy.actor = action.actor
                    action_copy.target = action.target
                    available_actions[part].append((j + 1, action_copy))
                    action_index_map.append((j + 1, action_copy, part))  # 记录编号、动作、身体部位
                    j += 1                

        # 显示可选行动
        for part, action_ids in available_actions.items():
            for action_id in action_ids:
                (id, paction) = action_id

        print("\n可选行动:")
        for body_part, actions_list in available_actions.items():
            # 为每个action设置actBodyPart
            for num, action in actions_list:
                for idx, (n, act, part) in enumerate(action_index_map):
                    if num == n and body_part == part:
                        act.set_actBodyPart(body_part)
                        action_index_map[idx] = (num, act, body_part)
            action_texts = [f"{num}. {action.name.format(chosenCloth='衣物')}" for num, action in actions_list]
            if action_texts:
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

