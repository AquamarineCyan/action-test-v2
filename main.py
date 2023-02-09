#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# main.py

import sys
from ctypes import windll
from PySide6.QtWidgets import QApplication

from utils.gui import MainWindow

print("main.py")

if __name__ == "__main__":
    # 是否以管理员身份运行
    if windll.shell32.IsUserAnAdmin():
        print("Admin")
        app = QApplication([])
        main_win_ui = MainWindow()
        main_win_ui.show()
        app.exec()
    else:
        # 调起UAC以管理员身份运行
        windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)
