import yaml
import random

class Action:
    def __init__(self, id, yamlPath, actor, target, actBodyPart=None, targetBodyPart=None, chosenCloth=None):
        # 从yamlPath中找到id
        self.id = id
        self.actor = actor
        self.target = target
        with open(yamlPath, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            action_data = data.get(id)
            if action_data is None:
                raise ValueError(f"ERROR: Action with id {id} not found in {yamlPath}")
            self.name = action_data.get('name', self.id)
            self.canContinue = action_data.get('canContinue', False)
            self.effects = action_data.get('effects', {})
            self.conditions = action_data.get('conditions', {})
            self.description = action_data.get('description',{'start':''})
            # 定义剩下的可选属性
            # TODO: 思考一下这是不是必须的，我现在脑子转不动了已经
            self.actBodyPart = actBodyPart
            self.targetBodyPart = targetBodyPart
            self.chosenCloth = chosenCloth

    def __str__(self):
        # TODO: 仍需完善。这会用在历史记录里。
        return f"{self.actor.name} {self.name} {self.chosenCloth if hasattr(self, 'chosenCloth') else self.target.name}"

    def can_execute(self):
        """检查行动是否可执行"""
        #return self.condition is None or self.condition(self.actor, self.target)
        # TODO
        all = True
        any = False
        # all
        for condition in self.conditions.get('all', []):
            owner = self.actor if condition['owner'] == 'actor' else self.target
            if condition['type'] == 'bodyPart':
                body_part = condition['bodyPart']
                is_occupied = condition['isOccupied']
                if owner.bodyParts[body_part]['isOccupied'] != is_occupied:
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

        # any
        for condition in self.conditions.get('any', []):
            owner = self.actor if condition['owner'] == 'actor' else self.target
            if condition['type'] == 'bodyPart':
                body_part = condition['bodyPart']
                is_occupied = condition['isOccupied']
                if owner.bodyParts.get(body_part, {}).get('isOccupied', None) == is_occupied:
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
        return all and any
    
    def execute(self):
        if not self.can_execute():
            print("行动无法执行，执行中断。")
            return  # Add a return statement to handle the case when the action cannot be executed
            
        # TODO: 区别处理target和actor
        for role, changes in self.effects.items():
            if role == "actor":
                affected_character = self.actor
            elif role == "target":
                affected_character = self.target
            else:
                continue  # 忽略无效的角色 key
            
            # 处理状态变更
            if "state" in changes:
                for state_name, value in changes["state"].items():
                    affected_character.change_state(state_name, value)

            # 处理衣物变更
            if "clothing" in changes:
                for cloth_name, action in changes["clothing"].items():
                    # 解析 chosenCloth
                    if cloth_name == "chosenCloth":
                        if self.chosenCloth:  # 确保 `chosenCloth` 有值
                            cloth_name = self.chosenCloth
                        else:
                            continue  # 没有 `chosenCloth`，则跳过

                    # 执行脱衣操作
                    if action == "remove":
                        affected_character.remove_clothing(self.target, cloth_name)
            # 处理start效果
            print(self.description)
            if "start" in self.description:
                start_desc = self.description["start"]
                if isinstance(start_desc, list):
                    chosen_desc = random.choice(start_desc)
                    print(f"Start description chosen: {chosen_desc}")
                    return chosen_desc.format(actor=self.actor.name,target=self.target.name)
                else:
                    print(f"Start effect: {start_desc}")
                    return [start_desc]
            return []
    
    def get_effects(self):
        """根据self.effects生成行动效果文本"""
        # TODO
        return self.effects
