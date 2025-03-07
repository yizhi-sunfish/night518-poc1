from abc import ABC, abstractmethod
from action import Action
from clothing import Clothing
import yaml

class Character(ABC):
    def __init__(self, character_file, is_player=False):
        # TODO: 从文件读取角色状态
        print("读取角色文件：", character_file)
        with open(character_file, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.name = data.get('name','')
        self.nickname = data.get('nickname','')
        self.state = (data.get('state', {}))
        self.bodyParts = data.get('bodyParts', {})
        self.clothing = data.get('clothing', {})
        #print("角色名：", self.name)
        #print("角色初始状态：")
        #print(self.state)
        #print("角色初始身体部位：")
        #print(self.bodyParts)
        #print("角色初始衣物：")
        #print(self.clothing)

        self.is_player = is_player

        self.history = []
        self.currentActions = []
        self.currentReactions = []
        self.nextActions = []
        self.previousRoundResult = ""
        
    def change_state(self, key, amount):
        """修改角色状态"""
        if key in self.state:
            self.state[key] = max(0, min(100, self.state[key] + amount))
        else:
            print(f"状态 {key} 不存在")
    
    def get_bodyPart(self):
        return self.bodyParts
    
    def is_bodyPartOccupied(self, key):
        return self.bodyParts[key]["isOccupied"]
    
    def is_bodyPartCovered(self, key):
        return self.bodyParts[key]["isCovered"]
    
    # TODO: 重构，使函数更加通用合理
    def change_bodyPart(self, key, isOccupied, isCovered):
        """修改角色身体部位状态"""
        if key in self.bodyParts:
            self.bodyParts[key]["isOccupied"] = isOccupied
            self.bodyParts[key]["isCovered"] = isCovered
        else:
            print(f"身体部位 {key} 不存在")

    def get_clothing(self):
        return self.clothing
    
    def remove_clothing(self, byWhom, cloth):
        if not self.clothing[cloth]:
            print(f"{byWhom.name} 无法脱下 {self.name} 的 {cloth.name}")
        else:
            if isinstance(self.clothing[cloth]["covers"], str):
                self.change_bodyPart(self.clothing[cloth]["covers"], False, False)
            elif isinstance(self.clothing[cloth]["covers"], list):
                for part in self.clothing[cloth]["covers"]:
                    self.change_bodyPart(part, False, False)
            self.clothing.pop(cloth)
    
    def updateHistory(self, action):
        self.history.append(action)

    def getHistory(self):
        return self.history
    

