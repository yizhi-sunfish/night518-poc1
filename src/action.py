class Action:
    def __init__(self, name, actor, target, effects, condition=None):
        self.name = name
        self.actor = actor # 行动发起者
        self.target = target # 行动对象
        self.canContinue = False # 行动是否默认持续多回合
        # TODO: 拓展effect的格式：
        # 1. 人物状态更新
        # 2. 人物衣物更新
        # 3. 人物身体部位更新
        self.effects = effects  # 字典 {"性欲": +10, "体感": -5}
        # TODO: 仍需考虑condition的实现形式
        self.condition = condition  # 例如 lambda player, partner: partner.state["开放"] < 50
        # TODO: 定义一个字符串，将动作转为合适的谓语，用于显示在UI上
        # 例如 "亲吻" -> "亲吻了"， "相互口交" -> "含住他的阴茎，并将自己的下体送入他口中"
        # 默认值为动作名
        self.description = self.name

    def __str__(self):
        return f"{self.actor.name} {self.name} {self.target.name}"

    def can_execute(self):
        """检查行动是否可执行"""
        return self.condition is None or self.condition(self.actor, self.target)

    def execute(self):
        """执行行动，改变状态"""
        # TODO: 将文本转移至text/，将生成文本的逻辑转移到get_effect(),打印文本的逻辑转移至UI
        # 这里只根据self.effect执行相应更新，并返回get_effect()
        if not self.can_execute():
            return f"{self.target.name} 轻轻推开了{self.actor.name}，他似乎没有准备好进行 {self.name}。"
        
        for key, value in self.effects.items():
            self.target.change_state(key, value)
        
        if self.target.state["性欲"] < 20:
            return f"{self.actor.name} {self.name}，{self.target.name} 闭起眼睛，微微颤抖，似乎有了些反应……"
        elif self.target.state["性欲"] < 50:
            return f"{self.actor.name} {self.name}，{self.target.name} 脸色泛红，他的胸口起伏着，小动作也多起来。看上去他有些兴奋。"
        elif self.target.state["性欲"] < 80:
            return f"{self.actor.name} {self.name}，{self.target.name} 呼吸急促，口中泄露出细碎的呻吟声。他的双眼紧闭，全身颤抖，看上去已经无法自控——他已经快要达到高潮了。"
        else:
            return f"{self.actor.name} {self.name}，{self.target.name} 紧紧地抓住你，他已经不再隐藏自己的欲望，痉挛着身体，发出了一声声甜腻的呻吟，求你让他攀上欢愉的高峰。"
        
    def get_effect(self):
        """根据self.effects生成行动效果文本"""
