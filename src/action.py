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
            return f"{partner.name} 轻轻推开了你，他似乎没有准备好进行 {self.name}。"
        
        for key, value in self.effects.items():
            partner.change_state(key, value)
        
        if partner.state["性欲"] < 20:
            return f"你 {self.name}，{partner.name} 闭起眼睛，微微颤抖，似乎有了些反应……"
        elif partner.state["性欲"] < 50:
            return f"你 {self.name}，{partner.name} 脸色泛红，他的胸口起伏着，小动作也多起来。看上去他有些兴奋。"
        elif partner.state["性欲"] < 80:
            return f"你 {self.name}，{partner.name} 呼吸急促，口中泄露出细碎的呻吟声。他的双眼紧闭，全身颤抖，看上去已经无法自控——他已经快要达到高潮了。"
        else:
            return f"你 {self.name}，{partner.name} 紧紧地抓住你，他已经不再隐藏自己的欲望，痉挛着身体，发出了一声声甜腻的呻吟，求你让他攀上欢愉的高峰。"
    
    def __str__(self):
        return f"Action(name={self.name}, effects={self.effects})"

