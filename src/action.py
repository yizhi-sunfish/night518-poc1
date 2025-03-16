import yaml
import random

class Action:
    def __init__(self, id, yamlPath, actor, target, state='start', actBodyPart=None, targetBodyPart=None, chosenCloth=None):
        """
        根据参数和YAML配置文件，初始化行动。\n
        参数:\n
            id (str): 行动的ID，一般为其英文单词。此参数为必填项。\n
            yamlPath (str): YAML配置文件的路径。此参数为必填项。\n
            actor (Character): 执行动作的角色。此参数为必填项。\n
            target (Character): 动作的目标角色。此参数为必填项。\n
            state (str, 可选): 动作的状态，可以是'start'（默认）、'continue'或'end'。\n
            actBodyPart (str, 可选): 执行动作的角色的对应身体部位。\n
            targetBodyPart (str, 可选): 动作目标角色的对应身体部位。\n
            chosenCloth (str, 可选): 动作中选择的衣物。\n
        异常:\n
            ValueError: 如果在YAML配置文件中找不到指定ID的动作，将抛出此异常。\n
        """
        # TODO: 加入行动成功率，和失败时的文本
        self.id = id
        self.actor = actor
        self.target = target
        self.state = state
        self.actBodyPart = actBodyPart
        self.targetBodyPart = targetBodyPart
        self.chosenCloth = chosenCloth
        with open(yamlPath, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            action_data = data.get(id)
            if action_data is None:
                raise ValueError(f"ERROR: Action with id {id} not found in {yamlPath}")
            self.name = action_data.get('name', self.id)
            """指代行动的文本，会出现在UI中，例如：“轻吻”、“脱去你的高领紧身衣”
               注意该字符串中可能会出现如下placeholder：
               - {player}
               - {partner}
               - {chosenCloth}
               - {actBodyPart}
               - {targetBodyPart}
            """
            self.isContinuous = action_data.get('isContinuous', False)
            """动作是否可以持续，类型为bool"""
            self.possibleBodyParts = action_data.get('possibleBodyParts', [])
            """可能执行动作的身体部位，类型为list"""
            self.effects = action_data.get('effects', {})
            """行动的后果，类型为dict"""
            self.conditions = action_data.get('conditions', {})
            """行动的可执行条件，类型为dict"""
            self.description = action_data.get('description',{'start':''})
            """执行行动之后的描述文本，会出现在UI中。类型为dict"""

    def __str__(self):
        """
        返回描述动作的间断字符串，会用于历史记录的打印
        """
        # TODO: 仍需完善
        return f"{self.actor.name} 用 {self.actBodyPart} {self.name}"

    def can_execute(self):
        """检查行动是否可执行，返回类型bool"""
        # TODO
        all = True   # 当全部all条件满足时，all为True，否则为False
        any = False  # 当至少一个any条件满足时，any为True，否则为False

        # all条件判定
        for condition in self.conditions.get('all', []):
            owner = self.actor if condition['owner'] == 'actor' else self.target
            if condition['type'] == 'bodyPart':
                body_part = condition['bodyPart']
                is_occupied = condition.get('isOccupied',None)
                is_covered = condition.get('isCovered',None)
                currentState = condition.get('currentState',None)
                # TODO: logic is poor, needs refactor
                if currentState is not None \
                    and owner.bodyParts[body_part].get('currentState') != currentState:
                    all = False
                elif is_occupied is not None \
                    and owner.bodyParts[body_part].get('isOccupied') != is_occupied \
                    and owner.bodyParts[body_part].get('currentAction') != self.id:
                    all = False
                # Currently adding this elif for checking the 2nd round, which is called in UI. 
                # Needs refactor.
                elif is_occupied is not None \
                    and self.actBodyPart is not None \
                    and owner.bodyParts[body_part].get('isOccupied') != is_occupied \
                    and owner.bodyParts[body_part].get('OccupiedByBodyPart') != self.actBodyPart:
                    all = False
                if is_covered is not None and owner.bodyParts[body_part].get('isCovered') != is_covered:
                    all = False
            elif condition['type'] == 'state':
                state = condition['state']
                min_value = condition.get('min', None)
                max_value = condition.get('max', None)
                if min_value is not None and owner.state.get(state, 0) < min_value:
                    all = False
                if max_value is not None and owner.state.get(state, 0) > max_value:
                    all = False
            elif condition['type'] == 'clothing':
                if condition['clothing']=='{chosenCloth}' and not self.chosenCloth:
                    all = False
                chosenCloth = condition['clothing'].format(chosenCloth=self.chosenCloth)
                if not (chosenCloth in owner.clothing):
                    all = False

        # any条件判定
        for condition in self.conditions.get('any', []):
            owner = self.actor if condition['owner'] == 'actor' else self.target
            if condition['type'] == 'bodyPart':
                body_part = condition['bodyPart']
                is_occupied = condition.get('isOccupied',None)
                is_covered = condition.get('isCovered',None)
                currentState = condition.get('currentState',None)
                if (owner.bodyParts[body_part].get('isOccupied', None) == is_occupied \
                   and owner.bodyParts[body_part].get('currentState', None) == currentState):
                    any = True
                if owner.bodyParts[body_part].get('currentAction') == self.id:
                    if self.actBodyPart == None:
                        any = True
                    elif self.actBodyPart == owner.bodyParts[body_part].get('OccupiedByBodyPart'):
                        any = True
            elif condition['type'] == 'state':
                state = condition['state']
                min_value = condition.get('min', None)
                max_value = condition.get('max', None)
                if min_value is not None and owner.state.get(state, 0) >= min_value:
                    any = True
                if max_value is not None and owner.state.get(state, 0) <= max_value:
                    any = True
            elif condition['type'] == 'clothing':
                chosenCloth = condition['clothing'].format(chosenCloth=self.chosenCloth)
                if chosenCloth in self.target.clothing:
                    any = True
        
        if not self.conditions.get('any', []):
            any = True
        #print("all = {}, any = {}".format(all,any))
        return all and any
    
    def execute(self):
        """
        执行行动，
        完成effects中列出的所有后果，
        返回本次动作输出的结果文本，类型str
        """
        if not self.can_execute():
            print("行动无法执行，执行中断。")
            return  # Add a return statement to handle the case when the action cannot be executed
        
        for role, changes in self.effects.items():
            if role == "actor":
                affected_character = self.actor
            elif role == "target":
                affected_character = self.target
            else:
                continue  # 忽略无效的角色key
            
            # 处理状态变更
            if "state" in changes and self.state is not "end":
                for state_name, value in changes["state"].items():
                    affected_character.change_state(state_name, value)

            # 处理衣物变更
            if "clothing" in changes:
                for cloth_name, action in changes["clothing"].items():
                    # 解析 chosenCloth
                    if cloth_name == "chosenCloth":
                        if self.chosenCloth:  
                            cloth_name = self.chosenCloth
                        else:
                            continue
                    # 执行脱衣操作
                    if action == "remove":
                        affected_character.remove_clothing(self.target, cloth_name)

            # 处理身体部位变更
            if "bodyParts" in changes:
                for part, effect in changes["bodyParts"].items():
                    if part == "actBodyPart":
                        if self.actBodyPart:
                            part = self.actBodyPart
                        else:
                            continue
                    #print("current action state:"+self.state)
                    if self.state == 'start':
                        #print("即将占用身体部位"+part)
                        affected_character.occupy_bodyPart(part,self.id,self.actBodyPart)
                    elif self.state == 'end':
                        #print("即将解放身体部位"+part)
                        affected_character.release_bodyPart(part)
                    if "currentState" in effect:
                        affected_character.update_bodyPart(part, currentState=effect['currentState'])
        
        # 处理返回文本
        if self.state in self.description:
            desc = self.description[self.state]
            if isinstance(desc, list):
                chosen_desc = random.choice(desc)
                return chosen_desc.format(actor=self.actor.name,
                                            target=self.target.name,
                                            chosenCloth=self.chosenCloth,
                                            actorNickname=self.actor.nickname,
                                            actBodyPart=self.actBodyPart,
                                            targetBodyPart=self.targetBodyPart
                                            )
            else:
                return [desc]
        return []

    def set_actBodyPart(self, part):
        """设置actBodyPart为给定字符串"""
        self.actBodyPart = part

    def set_targetBodyPart(self, part):
        """设置targetBodyPart为给定字符串"""
        self.targetBodyPart = part
    
    def set_chosenCloth(self, cloth):
        """设置chosenCloth为给定字符串"""
        self.chosenCloth = cloth

