from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.live import Live
import time

console = Console()

def progress_bar(value, max_value=100, width=20, color="green"):
    """生成可视化进度条"""
    filled_length = int(width * value // max_value)  # 计算填充的长度
    empty_length = width - filled_length  # 计算剩余的长度
    bar = "█" * filled_length + "░" * empty_length  # 使用 Unicode 方块构造进度条
    return f"[{color}]{bar}[/] {value}%"  # 添加颜色

# 角色对话框
def show_dialogue(text):
    console.print(Panel(Text(text, style="bold magenta"), border_style="magenta"))

# 角色状态栏
def show_status():
    table1 = Table(title="[bold blue]佐音 状态[/]", header_style="bold blue")
    table1.add_column("属性", justify="center")
    table1.add_column("数值", justify="center")

    table1.add_row("性欲", progress_bar(6, color="magenta"))
    table1.add_row("体感", progress_bar(8, color="green"))
    table1.add_row("开放", progress_bar(19, color="red"))

    table2 = Table(title="[bold red]阿伦 状态[/]", header_style="bold red")
    table2.add_column("属性", justify="center")
    table2.add_column("数值", justify="center")

    table2.add_row("性欲", progress_bar(60, color="magenta"))
    table2.add_row("体感", progress_bar(20, color="green"))
    table2.add_row("精神", progress_bar(20, color="blue"))
    table2.add_row("专注", progress_bar(100, color="white"))

    console.print(Columns([table1, table2]))

# 动作选择
def show_actions():
    console.print(Panel(
        """[bold]
【嘴】 1. 轻吻  2. 深入亲吻  3. 责骂
【左手】 4. 爱抚  5. 脱下你的黑色短裤
【右手】 6. 继续爱抚  7. 停止爱抚
        [/]""", border_style="cyan", title="[bold white]可选行动[/]"
        ))

# 逐字显示文本（打字机效果）
def typewriter(text, delay=0.02):
    for char in text:
        console.print(char, end="", style="bold magenta", highlight=False)
        time.sleep(delay)
    console.print()

def typewriter_panel(text, delay=0.06):
    """打字机效果 + Rich Panel"""
    displayed_text = ""
    with Live(refresh_per_second=10) as live:
        for char in text:
            displayed_text += char
            panel = Panel(Text(displayed_text, style="bold"), border_style="magenta")
            live.update(panel)
            time.sleep(delay)  # 逐字延迟

# 渲染界面
def render():
    console.clear()
    show_status()
    time.sleep(0.5)
    #show_dialogue(
    typewriter_panel(
"""
你的吻像蝴蝶一样轻轻落在佐音的唇上，转瞬又离开。佐音咯咯地笑起来：“好痒啊。”

你继续爱抚着佐音的身体，佐音的脸上泛起了一丝红晕，他的眼睛里闪烁着期待的光芒。
""")
    time.sleep(0.5)
    show_actions()
    console.print("选择多个行动（用空格分隔编号，例如：1 3 5）: ")

render()
