class Action:
    def __init__(self, name, effects, condition=None):
        self.name = name
        self.effects = effects  # 字典 {"性欲": +10, "舒适度": -5}
        self.condition = condition  # 例如 lambda player, partner: partner.state["开放"] < 50

    def can_execute(self, player, partner):
        """检查行动是否可执行"""
        return self.condition is None or self.condition(player, partner)

    def execute(self, player, partner):
        """执行行动，改变状态"""
        if not self.can_execute(player, partner):
            return f"{partner.name} 似乎没有准备好进行 {self.name}。"
        
        for key, value in self.effects.items():
            partner.change_state(key, value)
        
        return f"你 {self.name}，{partner.name} 似乎有了些反应……"

