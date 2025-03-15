# 整个类需要被重构，严格来说这里的内容不能被称之为event
# 它们对整个游戏的氛围很重要，需要一些更好的处理，但我也没想好该把它们放在哪里
import time
class Event:
    @staticmethod
    def check_triggers(player, partner, ui):
        """检查是否触发特殊事件"""
        if partner.state["开放"] < 20:
            ui.console.print(f"\n{partner.name}看起来有些不安，你也许应该温柔一点。")
        elif partner.state["开放"] < 50:
            ui.console.print(f"\n{partner.name}正在逐渐适应你的节奏。")
        elif partner.state["开放"] <= 80:
            ui.console.print(f"\n{partner.name}进入了状态，现在的他享受着和你的接触。")
        elif partner.state["性欲"] > 80 and partner.state["体感"] < 50:
            ui.console.print(f"\n{partner.name}渴望地看着你，似乎想让你更主动一些。")
        elif partner.state["性欲"] >80 and partner.state["体感"] > 50:
            ui.console.print(f"\n{partner.name} 看起来沉浸在你带给他的快感当中。")
        else:
            ui.console.print(f"\n{partner.name}彻底放松下来，在你取悦他的时候，他也偷偷摸摸地做些小动作触摸你。")
        time.sleep(0.7)

        if player.state["体感"] <= 30:
            ui.console.print(f"\n你感觉到疼痛，哪里都在痛，尤其是胸口。今天埃里给你注射了药，但这药似乎越来越不管用了，他说是因为你的身体产生了抗药性。操他妈的抗药性。", style="bold red")
        elif player.state["体感"] <= 50:
            ui.console.print(f"\n仅仅是呆在佐音的身边，你就感觉舒服了一点。这样的想法让你越发想要进一步触碰他。",style="yellow")
        elif player.state["体感"] <= 80:
            ui.console.print(f"\n兴奋的感觉渐渐盖过了痛苦，你渴求着更多亲密的接触。",style="cyan")
        time.sleep(0.7)

        if player.state["精神"] <= 25:
            ui.console.print(f"\n{player.name}感觉糟透了，一种熟悉的焦躁在{player.name}身体里蔓延，有什么东西快要溢出来，总之不会是什么好东西。\n{partner.name}正在看着{player.name}，目光里透露着担忧……有什么好担忧的？看了就让人烦躁。", style = "bold red")
        elif player.state["精神"] <= 40:
            ui.console.print(f"\n{player.name}始终不能放松下来，不快的感觉萦绕着{player.name}。还好{player.name}清楚自己是什么状态。{player.name}有{partner.name}在{player.name}身边，他的陪伴和触摸让{player.name}渐渐好起来。\n不会有问题的，是吧？", style = "yellow")
        elif player.state["精神"] <= 60:
            ui.console.print(f"\n虽然不容易，但你感觉自己平静了下来。你终于有心情去看佐音的面庞。多么美丽的孩子，他在看你，你也望着他的眼睛，蓝色的，像一汪湖水。\n这片湖泊属于你。", style="cyan")
        else:
            ui.console.print(f"\n你现在感觉棒极了，在佐音离开期间，从没有人让你感觉这么好过。你很高兴他终于回来了。\n如果时间能停留在这个时刻该多好，你想。", style="green")

