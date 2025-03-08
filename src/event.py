class Event:
    @staticmethod
    def check_triggers(player, partner):
        """检查是否触发特殊事件"""
        if partner.state["开放"] < 20:
            print(f"\n{partner.name}看起来有些不安，你也许应该温柔一点。")
        elif partner.state["开放"] < 50:
            print(f"\n{partner.name}正在逐渐适应你的节奏。")
        elif partner.state["开放"] <= 80:
            print(f"\n{partner.name}进入了状态，现在的他享受着和你的接触。")
        elif partner.state["性欲"] > 80 and partner.state["体感"] < 50:
            print(f"\n{partner.name}渴望地看着你，似乎想让你更主动一些。")
        elif partner.state["性欲"] >80 and partner.state["体感"] > 50:
            print(f"\n{partner.name} 看起来沉浸在你带给他的快感当中。")

#        if player.state["精神"] <= 25:
#            print(f"\n{player.name}能感觉到一种熟悉的焦躁在身体里蔓延，像是有什么东西快要溢出来。\n{partner.name}正在看着{player.name}，目光里透露着担忧……有什么好担忧的？看了就让人烦躁。")

