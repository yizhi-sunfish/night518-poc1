import yaml

class Character():
    def __init__(self, character_file, is_player=False):
        """
        通过读取 YAML 文件初始化 Character 对象。\n
        参数:\n
            character_file (str): 包含角色数据的 YAML 文件路径。此参数为必填项。\n
            is_player (bool, optional): 标志角色是否为玩家。默认为 False。\n
        属性:\n
            name (str): 角色的名字。\n
            nickname (str): 角色的昵称。\n
            state (dict): 角色的状态。\n
            bodyParts (dict): 角色的身体部位。\n
            clothing (dict): 角色的衣物。\n
            is_player (bool): 标志角色是否为玩家。\n
            history (list): 用于存储角色动作历史的列表。\n
        """
        print("读取角色文件：", character_file)
        with open(character_file, 'r', encoding='UTF-8') as file:
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
        
    def change_state(self, key, amount):
        """修改角色状态\n
           - key：状态的名称
           - amount：状态的变化值
        """
        if key in self.state:
            self.state[key] = max(0, min(100, self.state[key] + amount))
        else:
            print(f"状态 {key} 不存在")
    
    def get_bodyPart(self):
        """返回角色所拥有的身体部位"""
        return self.bodyParts
    
    def is_bodyPartOccupied(self, key):
        """返回角色某一个身体部位是否被占据"""
        # TODO：可以重构，判断占据身体部位的是不是特定动作或动作执行者的特定身体部位
        return self.bodyParts[key]["isOccupied"]
    
    def is_bodyPartCovered(self, key):
        """返回角色某一个身体部位是否被覆盖"""
        return self.bodyParts[key]["isCovered"]
    
    # TODO: 重构，使函数更加通用合理
    def update_bodyPart(self, key, isOccupied=None, isCovered=None, currentAction=None, currentState=None):
        """更新角色身体部位的被占用信息"""
        if key in self.bodyParts:
            if isOccupied != None:
                self.bodyParts[key]["isOccupied"] = isOccupied
            if isCovered != None:
                self.bodyParts[key]["isCovered"] = isCovered
            if currentAction != None:
                self.bodyParts[key]["currentAction"] = currentAction
            if currentState != None:
                self.bodyParts[key]["currentState"] = currentState
        else:
            print(f"身体部位 {key} 不存在")

    def get_clothing(self):
        """返回角色当前衣物"""
        return self.clothing
    
    def remove_clothing(self, byWhom, cloth):
        """除下角色的某件衣物"""
        if not self.clothing[cloth]:
            print(f"{byWhom.name} 无法脱下 {self.name} 的 {cloth.name}")
        else:
            if isinstance(self.clothing[cloth]["covers"], str):
                self.update_bodyPart(self.clothing[cloth]["covers"], False, False)
            elif isinstance(self.clothing[cloth]["covers"], list):
                for part in self.clothing[cloth]["covers"]:
                    self.update_bodyPart(part, None, False)
            self.clothing.pop(cloth)

    def occupy_bodyPart(self, bodyPart, action, actBodyPart):
        """
        占用给定身体部位。\n
        所需参数：\n
        - 占用身体部位的名字
        - 动作的id
        - 执行动作者所用身体部位的名字
        """
        # TODO: 重构，比如这里其实可以用if self.is_bodyPartOccupied(bodyPart)
        if self.bodyParts[bodyPart]['isOccupied'] == True:
            print(bodyPart + "已被占用，当前动作：" + self.bodyParts[bodyPart]['currentAction'])
            return False
        else:
            self.bodyParts[bodyPart]['isOccupied'] = True
            self.bodyParts[bodyPart]['currentAction'] = action
            self.bodyParts[bodyPart]['OccupiedByBodyPart'] = actBodyPart
            return True
    
    def release_bodyPart(self, bodyPart):
        """释放身体部位"""
        if self.bodyParts[bodyPart]['isOccupied'] == False:
            print(bodyPart + "空闲")
        else:
            self.bodyParts[bodyPart]['isOccupied'] = False
            self.bodyParts[bodyPart]['currentAction'] = ''        
    
    def updateHistory(self, action):
        """更新历史记录"""
        self.history.append(action)

    def getHistory(self):
        """输出历史记录"""
        return self.history
    

