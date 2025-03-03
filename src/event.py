class Event:
    @staticmethod
    def check_triggers(partner):
        """检查是否触发特殊事件"""
        if partner.state["舒适度"] < 20:
            print(f"\n{partner.name} 看起来有些不安，你也许应该温柔一点。")
        elif partner.state["性欲"] > 80 and partner.state["精神"] > 50:
            print(f"\n{partner.name} 渴望地看着你，似乎想让你更主动一些。")

