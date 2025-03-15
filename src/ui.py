from action import Action
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.live import Live
import time
import os
import yaml
import copy

class UI:
    def __init__(self):
        """初始化Console对象"""
        self.console = Console()

    def progress_bar(self, value, max_value=100, width=20, color="green"):
        """生成可视化进度条"""
        # TODO: 加入每个属性的数值所对应的含义，例如：体感 30% 难受
        filled_length = int(width * value // max_value)  # 计算填充的长度
        empty_length = width - filled_length  # 计算剩余的长度
        bar = "█" * filled_length + "░" * empty_length  # 使用 Unicode 方块构造进度条
        return f"[{color}]{bar}[/] {value}%"  # 添加颜色
# 逐字显示文本（打字机效果）
    def typewriter(self, text, delay=0.04, text_style="bold", line_break=True):
        """打字机效果"""
        for char in text:
            self.console.print(char, end="", style=text_style, highlight=False)
            time.sleep(delay)
        if line_break:
            self.console.print()

    def typewriter_panel(self, text, delay=0.04):
        """打字机效果 + Rich Panel"""
        displayed_text = ""
        with Live(refresh_per_second=10) as live:
            for char in text:
                displayed_text += char
                panel = Panel(Text(displayed_text), border_style="magenta")
                live.update(panel)
                time.sleep(delay)  # 逐字延迟

    def display_status(self, player, partner):
        """显示当前两位角色的状态"""

        # TODO: use a generic format that both name and nickname can be used
        table_player = Table(title=f"[bold red]{player.nickname} 状态[/]")
        table_partner = Table(title=f"[bold cyan]{partner.name} 状态[/]")
        table_player.add_column("属性", justify="center")
        table_player.add_column("数值", justify="center")
        table_partner.add_column("属性", justify="center")
        table_partner.add_column("数值", justify="center")

        # TODO: Read from file instead of hardcoded
        table_player.add_row("性欲", self.progress_bar(player.state['性欲'], color="magenta"))
        table_player.add_row("体感", self.progress_bar(player.state['体感'], color="green"))
        table_player.add_row("精神", self.progress_bar(player.state['精神'], color="blue"))
        #table_player.add_row("专注", self.progress_bar(player.state['专注'], color="grey"))

        table_partner.add_row("性欲", self.progress_bar(partner.state['性欲'], color="magenta"))
        table_partner.add_row("体感", self.progress_bar(partner.state['体感'], color="green"))
        table_partner.add_row("开放", self.progress_bar(partner.state['开放'], color="red"))

        self.console.print(Columns([table_player, table_partner], equal=True, expand=True, align="center"))

    def get_init_action_list(self, player, partner):
        """生成所有动作的列表"""
        # TODO: 尽可能让所有数据都自动生成，避免hardcode
        with open('data/actions/index.yaml', 'r', encoding='utf-8') as file:
            self.actions_index_data = yaml.safe_load(file)
        self.init_actions = [Action(id, 'data/actions/' + file_name, player, partner, 'start') for id, file_name in self.actions_index_data.items()]
        
        # 额外加入脱衣选项
        self.init_actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, 'start', None, None, '白色背心'))
        self.init_actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, 'start', None, None, '四角内裤'))
        self.init_actions.append(Action('take_off', 'data/actions/clothing.yaml', player, partner, 'start', None, None, '高领紧身衣'))
        self.init_actions.append(Action('take_off', 'data/actions/clothing.yaml', player, partner, 'start', None, None, '黑色短裤'))

    # deprecated
    def get_single_choice(self, player, partner):
        """获取玩家选择的单个行动(deprecated)"""
        with open('data/actions/index.yaml', 'r', encoding='utf-8') as file:
            self.actions_index_data = yaml.safe_load(file)
        actions = [Action(id, 'data/actions/'+file_name, player, partner, 'start') for id, file_name in self.actions_index_data.items()]
        # TODO：目前先手动加入脱衣选项，之后再想怎么更好地实现
        actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, 'start', '右手',None,'白色背心'))
        actions.append(Action('undress', 'data/actions/clothing.yaml', player, partner, 'start', '左手',None,'四角内裤'))
        
        j = 0
        action_text = []
        map = [0] * len(actions)
        for i, action in enumerate(actions):
            if action.can_execute():
                action_text += f"{j + 1}. {action.name.format(chosenCloth=action.chosenCloth)}\n"
                map[j] = i
                j += 1
        choice = int(input("选择行动 (输入编号): ")) - 1
        self.console.print(Panel(action_text, border_style="cyan", title="[bold white]可选行动[/]"))
        return actions[map[choice]]
    
    def get_multiple_actions(self, player, partner):
        """打印当前可选行动，并获取玩家的选择。支持多个行动的输入。"""
        # TODO: 重构。函数包含了太多逻辑，需要breakdown和去除冗余
        if not hasattr(self,'init_action_list'):
            self.get_init_action_list(player, partner)
        # 存储按身体部位分类的可执行动作
        available_actions = {}
        action_index_map = []
        j = 0  # 仅计算可执行的选项编号
        default_actions = {}

        # 遍历玩家可用的身体部位
        # 在每个loop，查询当前身体部位是否被占用，如是，加入停止动作
        # 如否，查询当前部位可用动作
        for part in player.bodyParts:
            if part not in available_actions:
                available_actions[part] = []
            if player.bodyParts[part]['isOccupied']:
                # 加入继续和停止的动作
                # TODO: 这里有个bug需要修正
                # 如果一个动作占用多个身体部位，那么下一轮多个身体部位会给出继续和停止的选项
                # 但只有真正的actBodyPart才能够行动
                path = {id:path for id, path in self.actions_index_data.items() if id == player.bodyParts[part]['currentAction']}
                continue_action = Action(player.bodyParts[part]['currentAction'], 'data/actions/' + path[player.bodyParts[part]['currentAction']],player,partner,'continue',part)
                end_action = Action(player.bodyParts[part]['currentAction'], 'data/actions/' + path[player.bodyParts[part]['currentAction']],player,partner,'end',part) 
                continue_action.name = "继续" + continue_action.name
                end_action.name = "停止" + end_action.name
                available_actions[part].append((j + 1, continue_action))
                action_index_map.append((j + 1, continue_action, part))
                default_actions[part] = str(j + 1)
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
                    action_copy.set_actBodyPart(part)
                    # check 2nd round
                    if not action_copy.can_execute():
                        continue
                    available_actions[part].append((j + 1, action_copy))
                    action_index_map.append((j + 1, action_copy, part))  # 记录编号、动作、身体部位
                    j += 1                

        # 显示可选行动
        for part, action_ids in available_actions.items():
            for action_id in action_ids:
                (id, paction) = action_id

        action_texts = "\n"
        active_parts = []
        for body_part, actions_list in available_actions.items():
            # 为每个action设置actBodyPart
            #for num, action in actions_list:
            #    for idx, (n, act, part) in enumerate(action_index_map):
            #        if num == n and body_part == part:
            #            act.set_actBodyPart(body_part)
            #            action_index_map[idx] = (num, act, body_part)
            action_part_texts = []
            for num, action in actions_list:
                action_part_texts.append(f"{num}. {action.name.format(player=player.name,partner=partner.name,chosenCloth=action.chosenCloth)}")
                if str(num) in default_actions.values():
                    action_part_texts[-1] += "（默认）"
            if action_part_texts:
                action_texts += f"【{body_part}】 " + "  ".join(action_part_texts) + "\n"
                active_parts.append(body_part)
                
        self.console.print(Panel(action_texts, border_style="cyan", title="[bold white]可选行动[/]"))

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

        for active_part in active_parts:
            if active_part not in occupied_parts and active_part in default_actions.keys():
                #print("监测到可用身体部位没有动作且默认动作存在")
                default_action = next(a for num, a, p in action_index_map if num == int(default_actions[active_part]))
                selected_actions.append(default_action)
                occupied_parts.add(active_part)

        return selected_actions  # 返回选定的多个动作
    
    def display_result(self, result):
        """以rich panel格式显示上一回合结果的文本"""
        self.console.print(Panel(Text(result, style="bold magenta"), border_style="magenta"))

    def display_end_message(self, player, partner):
        """输出历史操作"""
        print(f"你的历史操作:")
        for action in player.getHistory():
            time.sleep(0.7)
            print(str(action).format(player=player.name,
                                partner=partner.name,
                                chosenCloth=action.chosenCloth,
                                actBodyPart=action.actBodyPart,
                                targetBodyPart=action.targetBodyPart))
    
    def clean_screen(self):
        """清除屏幕"""
        self.console.clear()

