"""自定义信号"""

from PySide6.QtCore import QObject, Signal


class MySignals(QObject):
    """自定义信号类"""
    text_print_update = Signal(str)  # 主界面信息文本更新
    text_num_update = Signal(str)  # 完成情况文本更新
    is_fighting_update = Signal(bool)  # 运行状态更新
    qmessagbox_update = Signal(str, str)  # 弹窗更新


global_ms = MySignals()
