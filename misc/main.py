import random
import os

# 定义角色类(佐音)
class Character:
    def __init__(self, name):
        self.name = name
        self.arousal = 10   # 性欲
        self.comfort = 50  # 舒适度/体感
        self.openness = 0 # 开放度
        self.reactions = "" # 反应文本
    
    def update_state(self, arousal_change=0, comfort_change=0, openness_change=0):
        self.arousal = max(0, min(100, self.arousal + arousal_change))
        self.comfort = max(0, min(100, self.comfort + comfort_change))
        self.openness = max(0, min(100, self.openness + openness_change))
    
    def get_status_text(self):
        return f"性欲: {self.arousal} / 体感: {self.comfort} / 开放度: {self.openness}"
    
    def get_reaction_text(self):
        return self.reactions
    
    def set_reaction(self):
        # 佐音的反应根据舒适度来判定
        if self.comfort < 20:
            self.reactions = "佐音的脸色变得苍白，他的眼神中透露出不安。"
        elif self.comfort < 40:
            self.reactions = "佐音的脸上泛起了红晕，他的眼神有些迷离。"
        elif self.comfort < 60:
            self.reactions = "佐音的身体十分放松，他的眼神中透露出满足。"
        elif self.comfort < 80:
            self.reactions = "佐音的身体微微颤抖，他的眼神中闪烁着期待。"
        else:
            self.reactions = "佐音的身体紧绷，他的脸越来越红，呼吸也变得急促。"
class Player:
    def __init__(self):
        self.sensation = 50  # 体感
        self.mental = 50  # 精神状态
        self.focus = 50   # 专注
        self.arousal = 0  # 性欲
    
    def get_status_text(self):
        return f"体感: {self.sensation} / 精神: {self.mental} / 专注: {self.focus} / 性欲: {self.arousal}"

def display_ui(character, player, last_action):
    os.system('cls||clear')
    print(f"【上回合行动后果】{last_action}")
    print(f"【佐音的反应和行为】{character.get_reaction_text()}")
    print(f"【佐音的状态】{character.get_status_text()}")
    print("【提示】如果他不够开放，你可能需要更温柔地引导。")
    print("\n【状态区】")
    print(f"阿伦状态：{player.get_status_text()}")
    print("\n【行动区】")
    print("1. 亲吻（嘴）  2. 抚摸（双手）  3. 紧贴（双腿）  4. 撩拨（腰腹）  5. 直接触碰（阴茎）  6. 挑逗（臀部）")

def main():
    zayn = Character("佐音")
    player = Player()
    last_action = "初始状态，你们刚刚开始亲密互动。"
    
    while True:
        display_ui(zayn, player, last_action)
        
        choice = input("选择你的行动（输入1-6，或输入 q 退出）：")
        if choice.lower() == 'q':
            print("游戏结束。")
            break
        
        action_map = {
            "1": ("你亲吻了佐音的额头，他微微闭上眼睛，似乎感到安心。", 0, 5, 2),
            "2": ("你的手指轻轻抚摸他的后背，他的肌肉稍微放松了一些。", 0, 5, 1),
            "3": ("你用双腿紧贴他的身体，他有些害羞地微微颤抖。", 5, 2, 3),
            "4": ("你的手指滑过他的腹部，他的呼吸变得急促。", 8, -2, 4),
            "5": ("你直接触碰他的下体，他的身体明显紧绷了一下。", 15, -5, 10),
            "6": ("你轻轻拍了拍他的臀部，他害羞地缩了一下，但没有拒绝。", 5, -1, 3)
        }
        
        if choice in action_map:
            text, arousal, comfort, openness = action_map[choice]
            zayn.set_reaction()
            zayn.update_state(arousal, comfort, openness)
            last_action = text
            
            # 判定高潮或中断
            if zayn.arousal >= 99 and zayn.comfort>=90 and zayn.openness >= 60:
                print("\n【高潮判定】佐音已经完全沉浸在快感中，他的身体不受控制地抽搐起来，手指抓挠着你，呻吟着达到了巅峰……乳白色的液体从他的阴茎喷涌而出。过了许久，他才慢慢恢复了平静，脸上泛起一片红晕。" +\
                      "\n “我爱你。”他凑到你的耳边轻轻对你说，然后在你脸上亲了一下。")
                break
            elif zayn.comfort < 20:
                print("\n【中断】佐音似乎感到不适，停止了动作。")
                break
        else:
            print("无效输入，请选择 1-6 或输入 q 退出。")

if __name__ == "__main__":
    main()

