from abc import ABC, abstractmethod
from action import Action
from clothing import Clothing

class Character(ABC):
    def __init__(self, name, is_player=False):
        self.name = name
        self.is_player = is_player
        self.state = {
            "精神": 100,  # 影响耐心、抗拒程度
            "性欲": 0,   # 影响接受度
            "舒适度": 50, # 低时会抗拒
            "专注": 100, # 低时难以控制行为
            "高潮": False, # 达到高潮则游戏结束
            "开放": 100, # 低时会抗拒
        }
        self.history = []
        self.currentActions = []
        self.currentReactions = []
        self.nextActions = []
        self.previousRoundResult = ""
        self.clothing = []

    def change_state(self, key, amount):
        """修改角色状态"""
        if key in self.state:
            self.state[key] = max(0, min(100, self.state[key] + amount))
        if key == "性欲" and self.state[key] >= 100:
            self.state["高潮"] = True

    def get_clothing(self):
        return self.clothing
    
    def remove_clothing(self, byWhom, cloth):
        if not self.clothing.remove(cloth):
            print(f"{byWhom.name} 无法脱下 {self.name} 的 {cloth.name}")
    
    def updateState(self, arousal_change=0, comfort_change=0, openness_change=0):
        self.state["性欲"] = max(0, min(100, self.state["性欲"] + arousal_change))
        self.state["舒适度"] = max(0, min(100, self.state["舒适度"] + comfort_change))
        self.state["开放"] = max(0, min(100, self.state["开放"] + openness_change))

    

