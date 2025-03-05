from abc import ABC, abstractmethod
from action import Action
from clothing import Clothing

class Character(ABC):
    def __init__(self, name, is_player=False, nickname=""):
        self.name = name
        self.nickname = nickname
        self.is_player = is_player
        # TODO: 从文件读取角色状态
        self.state = {
            "精神": 100, # 影响耐心、抗拒程度
            "性欲": 10,   
            "体感": 50,  # 低时会抗拒
            "专注": 100, # 低时难以控制行为
            "高潮": False, # 达到高潮则游戏结束
            "开放": 0, # 低时会抗拒
        }
        # TODO: 从文件读取角色衣物
        self.clothing = {
#            "白色背心": ["胸部"],
#            "四角内裤": ["阴茎", "臀部"],
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
    
    # TODO: 修改身体部位状态
    def change_bodyPart(self, bodyPart, amount):
        """修改角色身体部位状态"""
        pass

    def get_clothing(self):
        return self.clothing
    
    def remove_clothing(self, byWhom, cloth):
        if not self.clothing.remove(cloth):
            print(f"{byWhom.name} 无法脱下 {self.name} 的 {cloth.name}")
    
    def updateState(self, arousal_change=0, comfort_change=0, openness_change=0):
        self.state["性欲"] = max(0, min(100, self.state["性欲"] + arousal_change))
        self.state["体感"] = max(0, min(100, self.state["体感"] + comfort_change))
        self.state["开放"] = max(0, min(100, self.state["开放"] + openness_change))
    
    def updateHistory(self, action):
        self.history.append(action)

    def getHistory(self):
        return self.history

    

