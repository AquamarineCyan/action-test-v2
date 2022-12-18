#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# gui.py

import time
from pathlib import Path
from threading import Thread

from PySide6.QtGui import QIcon, QPixmap, QTextCursor
from PySide6.QtWidgets import QMainWindow, QMessageBox, QWidget


from .window import window
from .config import config
from .mysignal import global_ms as ms
from .mythread import MyThread
from .log import log
from .upgrade import *
from ui.new170 import Ui_MainWindow
from package import *


class MainWindow(QMainWindow):
    _list_function = [  # 功能列表
        "1.组队御魂副本",
        "2.组队永生之海副本",
        "3.业原火副本",
        "4.御灵副本",
        "5.个人突破",
        "6.寮突破",
        "7.道馆突破",
        "8.普通召唤",
        "9.百鬼夜行",
        "10.限时活动",
        "11.组队日轮副本"
    ]
    _package_ = [  # 图片素材文件夹
        "yuhun",
        "yongshengzhihai",
        "yeyuanhuo",
        "yuling",
        "jiejietupo",
        "daoguantupo",
        "zhaohuan",
        "baiguiyexing",
        "huodong"
    ]
    _choice: int  # 功能

    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_MainWindow()
        # 初始化界面
        self.setFixedSize(550, 450)  # 固定宽高
        self.ui.setupUi(self)
        # 窗口图标
        icon = QIcon()
        icon.addPixmap(QPixmap("buzhihuo.ico"))
        self.setWindowIcon(icon)
        self.setWindowTitle(f"Onmyoji_Python - v{config.version}")  # 版本号显示
        timenow = time.strftime("%H:%M:%S")
        try:
            log._write_to_file("[START]")
            log._write_to_file(f"{timenow} [VERSION] {config.version}")
        except:
            pass

        # 事件连接
        self.ui.button_resources.clicked.connect(self.resources)  # 资源检测按钮
        # self.ui.button_wininfo.clicked.connect(self.wininfo_update)  # 更新窗口信息
        self.ui.button_start.clicked.connect(self.start)  # 开始按钮
        self.ui.combo_choice.currentIndexChanged.connect(
            self.choice_text)  # 功能选择事件

        # 自定义信号
        ms.text_print_update.connect(self.text_print_update_func)  # 主界面信息文本更新
        # ms.text_wininfo_update.connect(
        # self.text_wininfo_update_func)  # 窗口信息文本更新
        ms.text_num_update.connect(self.text_num_update_func)  # 完成情况文本更新
        ms.is_fighting_update.connect(self.is_fighting)  # 运行状态更新
        ms.qmessagbox_update.connect(self.qmessagbox_update_func)  # 弹窗更新

        # 初始化控件
        self.ui.combo_choice.addItems(self._list_function)
        self.ui.button_start.setEnabled(False)
        self.ui.combo_choice.setEnabled(False)
        self.ui.spinB_num.setEnabled(False)
        self.ui.stackedWidget.setCurrentIndex(0)  # 索引0，空白
        self.ui.text_print.document().setMaximumBlockCount(50)

        # 程序开启运行
        # application_init
        thread_update = Thread(target=self.application_init)
        thread_update.daemon = True
        thread_update.start()

        # thread_resources = MyThread(func=self.resources_auto)
        # thread_resources.daemon = True
        # thread_resources.start()
        # thread_resources.join()
        # self.environment(thread_resources.get_result())

    def application_init(self):
        def resources_auto():
            thread_resources = MyThread(func=self.resources_auto)
            thread_resources.daemon = True
            thread_resources.start()
            thread_resources.join()
            self.environment(thread_resources.get_result())
            log.info("资源检测完成")

        log.ui("未正确使用所产生的一切后果自负\n保持您的肝度与日常无较大差距")
        log.ui(f"application path:{config.application_path}")
        log.ui(f"resource path:{config.resource_path}")
        window.get_game_window_handle()
        resources_auto()
        log.info("开机自启任务完成")

    def pic_is_complete(self) -> bool:
        for i in range(len(self._package_)):
            flag = Path(config.resource_path.joinpath(
                self._package_[i])).exists()
            if not flag:
                # QMessageBox.critical(self, "ERROR", f"无{self._package_[i]}文件夹")
                return False
        return True

    def qmessagbox_update_func(self, level: str, msg: str) -> None:
        match level:
            case "ERROR":
                QMessageBox.critical(self, level, msg)

    def text_print_update_func(self, text: str) -> None:
        """输出内容至文本框

        WARN -> 红色

        SCENE -> 绿色

        Args:
            text(str): 文本内容
        """
        if "[WARN]" in text:
            self.ui.text_print.setTextColor("red")
        elif "[SCENE]" in text:
            self.ui.text_print.setTextColor("green")

        self.ui.text_print.append(text)
        self.ui.text_print.ensureCursorVisible()  # 自动换行
        self.ui.text_print.moveCursor(
            self.ui.text_print.textCursor().End)  # 自动滑动到底
        self.ui.text_print.setTextColor("black")

    def text_num_update_func(self, text: str):
        """输出内容至文本框“完成情况”"""
        self.ui.text_num.setText(text)

    def text_wininfo_update_func(self, text: str):
        """输出窗口信息"""
        timenow = time.strftime("%H:%M:%S")
        self.ui.text_wininfo.setText(text)
        text = text.replace("\n", " ")
        text = f"{timenow} [WINDOW] {text}"
        print(f"[DEBUG] {text}")
        log._write_to_file(text)

    def environment(self, level):
        match level:
            case "log":
                QMessageBox.critical(self, "ERROR", "创建log目录失败，请重试！")
            case "picpath":
                QMessageBox.critical(self, "ERROR", "图片资源不存在！")
                log._write_to_file("[ERROR] no pic")
            case "pic is complete":
                QMessageBox.critical(self, "ERROR", "资源缺损！")
                log._write_to_file("[ERROR] no pic")
            case "no game":
                # QMessageBox.critical(self, "ERROR", "请打开游戏！")
                ms.qmessagbox_update.emit("ERROR","请打开游戏！")
                log._write_to_file("[ERROR] no game")
            case "no pre-game":
                QMessageBox.critical(self, "ERROR", "请前置游戏窗口！")
                log._write_to_file("[ERROR] no pre-game")
            case "no right size":
                choice = QMessageBox.question(
                    self, "窗口大小不匹配", "是否强制缩放，如不缩放，请自行靠近1136*640或者替换pic文件夹中对应素材")
                log._write_to_file("[ERROR] no right size")
                if choice == QMessageBox.Yes:
                    window.force_zoom()
                    log._write_to_file("user choose force_zoom")
                elif choice == QMessageBox.No:
                    log._write_to_file("user choose not force_zoom")
            case _:
                self.ui.button_resources.setEnabled(False)
                self.ui.button_resources.setText("环境完整")
                self.ui.combo_choice.setEnabled(True)
                self.ui.spinB_num.setEnabled(True)
                log.ui("移动游戏窗口后，点击下方“更新游戏窗口”即可\n请选择功能以加载内容")
                # 悬赏封印
                thread_xuanshang = Thread(
                    target=xuanshangfengyin.XuanShangFengYin().judge)
                thread_xuanshang.daemon = True
                thread_xuanshang.start()

    def resources_auto(self) -> str:
        """自动环境检测"""
        log.info("resources_auto")
        resource_path = config.resource_path
        # handle_coor = window.getInfo_Window()  # 游戏窗口
        handle_coor = window.handle_coor
        level: str = ""
        # log检测
        if not log.init():
            level = "log"
        # 图片资源检测
        elif not resource_path.exists():
            level = "no pic"
        # 图片资源是否完整
        elif not self.pic_is_complete():
            level = "pic is complete"
        # 游戏环境检测
        elif handle_coor == (0, 0, 0, 0):
            level = "no game"
        elif handle_coor[0] < -9 or handle_coor[1] < 0 or handle_coor[2] < 0 or handle_coor[3] < 0:
            level = "no pre-game"
        # 环境完整
        # TODO 解除窗口大小限制，待优化
        elif handle_coor[2] - handle_coor[0] != window.absolute_window_width and handle_coor[3] - handle_coor[
                1] != window.absolute_window_height:
            level = "no right size"

        return level
    # FIXME remove for old code

    def resources(self):
        """环境检测按钮"""
        handle_coor = window.get_game_window_handle()  # 游戏窗口
        # log检测
        if not log.init():
            QMessageBox.critical(self, "ERROR", "创建log目录失败，请重试！")
        # 图片资源检测
        elif not config.resource_path.exists():
            QMessageBox.critical(self, "ERROR", "图片资源不存在！")
            log._write_to_file("[ERROR] no pic")
        # 图片资源是否完整
        # elif not self.pic_is_complete():
        #     pass
        # 游戏环境检测
        elif handle_coor == (0, 0, 0, 0):
            QMessageBox.critical(self, "ERROR", "请打开游戏！")
            log._write_to_file("[ERROR] no game")
        elif handle_coor[0] < -9 or handle_coor[1] < 0 or handle_coor[2] < 0 or handle_coor[3] < 0:
            QMessageBox.critical(self, "ERROR", "请前置游戏窗口！")
            log._write_to_file("[ERROR] no pre-game")
        # elif handle_coor[2] - handle_coor[0] != window.absolute_window_width and handle_coor[3] - handle_coor[
        #     1] != window.absolute_window_height:
        #     QMessageBox.critical(self, "ERROR", "窗口大小不匹配!")
        #     log._write_to_file("[ERROR] no right size")
        # 环境完整
        else:
            self.ui.button_resources.setEnabled(False)
            self.ui.button_resources.setText("环境完整")
            self.ui.combo_choice.setEnabled(True)
            self.ui.spinB_num.setEnabled(True)
            log.ui("移动游戏窗口后，点击下方“更新游戏窗口”即可\n请选择功能以加载内容")
            # 悬赏封印
            thread_xuanshang = Thread(
                target=xuanshangfengyin.XuanShangFengYin().judge)
            thread_xuanshang.daemon = True
            thread_xuanshang.start()

        # 解除窗口大小限制，待优化
        if handle_coor[2] - handle_coor[0] != window.absolute_window_width and handle_coor[3] - handle_coor[
                1] != window.absolute_window_height:
            choice = QMessageBox.question(
                self, "窗口大小不匹配", "是否强制缩放，如不缩放，请自行靠近1136*640或者替换pic文件夹中对应素材")
            # QMessageBox.critical(self, "ERROR", "窗口大小不匹配!\n"
            #                                     "已解除窗口大小限制，请尽量靠近1136*640")
            log._write_to_file("[ERROR] no right size")
            if choice == QMessageBox.Yes:
                window.force_zoom()
                log._write_to_file("user choose force_zoom")
            elif choice == QMessageBox.No:
                log._write_to_file("user choose not force_zoom")

    # def wininfo_update(self):
    #     """更新窗口信息"""
    #     window.getInfo_Window()

    def choice_text(self):
        """功能描述"""
        text = self.ui.combo_choice.currentText()
        self.ui.button_start.setEnabled(True)
        self.ui.spinB_num.setEnabled(True)
        # self.is_fighting_yuhun(False)
        self.ui.stackedWidget.setCurrentIndex(0)  # 索引0，空白
        if text == self._list_function[0]:
            # 1.组队御魂副本
            self._choice = 1
            log.ui("请确保阵容稳定，仅适用于队友挂饼，不适用于极限卡速，默认打手\n待开发：手动第一次锁定阵容")
            self.ui.stackedWidget.setCurrentIndex(1)  # 索引1，御魂
            # 默认值
            self.ui.spinB_num.setValue(1)
            self.ui.spinB_num.setRange(1, 200)
            # self.is_fighting_yuhun(True)
            self.ui.button_driver_False.setChecked(True)
            self.ui.button_passengers_2.setChecked(True)
        elif text == self._list_function[1]:
            # 2.组队永生之海副本
            self._choice = 2
            log.ui("默认打手30次\n阴阳师技能自行选择，如晴明灭\n待开发：手动第一次锁定阵容")
            self.ui.stackedWidget.setCurrentIndex(1)  # 索引1，御魂
            # 默认值
            self.ui.spinB_num.setValue(30)
            self.ui.spinB_num.setRange(1, 100)
            # self.is_fighting_yuhun(True)
            self.ui.button_driver_False.setChecked(True)
            self.ui.button_passengers_2.setChecked(True)
        elif text == self._list_function[2]:
            # 3.业原火副本
            self._choice = 3
            log.ui("默认为“痴”，有“贪”“嗔”需求的，可替换pic路径下tiaozhan.png素材")
            self.ui.spinB_num.setValue(1)
            self.ui.spinB_num.setRange(1, 100)
        elif text == self._list_function[3]:
            # 4.御灵副本
            self._choice = 4
            log.ui("暗神龙-周二六日\n暗白藏主-周三六日\n暗黑豹-周四六\n暗孔雀-周五六日\n绘卷期间请减少使用")
            self.ui.spinB_num.setValue(1)
            self.ui.spinB_num.setRange(1, 100)
        elif text == self._list_function[4]:
            # 5.个人突破
            self._choice = 5
            log.ui("默认3胜刷新，上限30")
            # self.ui.stackedWidget.setCurrentIndex(2)  # 索引2，结界突破
            self.ui.spinB_num.setValue(1)
            self.ui.spinB_num.setRange(1, 30)
        elif text == self._list_function[5]:
            # 6.寮突破
            self._choice = 6
            now = time.strftime("%H:%M:%S")
            if now >= "21:00:00":
                log.warn("CD无限", True)
                log.ui("请尽情挑战，桌面版单账号上限100次")
            else:
                log.warn("CD受限", True)
                log.ui("默认6次，可在每日21时后无限挑战")
            log.ui("待开发：滚轮翻页")
            self.ui.spinB_num.setValue(6)
            self.ui.spinB_num.setRange(1, 200)
        elif text == self._list_function[6]:
            # 7.道馆突破
            self._choice = 7
            log.ui("目前仅支持正在进行中的道馆突破，无法实现跳转道馆场景\n待开发：冷却时间、观战助威")
            self.ui.stackedWidget.setCurrentIndex(3)  # 索引3，道馆突破
            self.ui.spinB_num.setEnabled(False)
        elif text == self._list_function[7]:
            # 8.普通召唤
            self._choice = 8
            log.ui("普通召唤，请选择十连次数")
            self.ui.spinB_num.setValue(1)
            self.ui.spinB_num.setRange(1, 100)
        elif text == self._list_function[8]:
            # 9.百鬼夜行
            self._choice = 9
            log.ui("仅适用于清票，且无法指定鬼王")
            self.ui.spinB_num.setValue(1)
            self.ui.spinB_num.setRange(1, 100)
        elif text == self._list_function[9]:
            # 10.限时活动
            self._choice = 10
            log.ui(
                "适用于限时活动及其他连点，请提前确保阵容完好并锁定，替换pic文件夹huodong下的title.png、tiaozhan.png，周年庆活动素材已替换")
            self.ui.spinB_num.setValue(1)
            self.ui.spinB_num.setRange(1, 999)
        elif text == self._list_function[10]:
            # 11.组队日轮副本
            self._choice = 11
            log.ui("请确保阵容稳定，仅适用于队友挂饼，不适用于极限卡速，默认打手\n待开发：手动第一次锁定阵容")
            self.ui.stackedWidget.setCurrentIndex(1)  # 索引1，御魂
            # 默认值
            self.ui.spinB_num.setValue(1)
            self.ui.spinB_num.setRange(1, 100)
            self.ui.button_driver_False.setChecked(True)
            self.ui.button_passengers_2.setChecked(True)

    def start(self):
        """开始按钮"""
        n = self.ui.spinB_num.value()
        self.ui.text_num.clear()
        self.is_fighting(True)
        thread = None  # 线程
        if self._choice == 1:
            # 1.组队御魂副本
            # 是否司机（默认否）
            # 组队人数（默认2人）
            driver = self.ui.buttonGroup_driver.checkedButton().text()
            if driver == "否":
                flag_driver = False
            else:
                flag_driver = True
            flag_passengers = int(
                self.ui.buttonGroup_passengers.checkedButton().text())
            thread = Thread(target=yuhun.YuHun().run, args=(
                n, flag_driver, flag_passengers))
        elif self._choice == 2:
            # 2.组队永生之海副本
            # 是否司机（默认否）
            driver = self.ui.buttonGroup_driver.checkedButton().text()
            if driver == "否":
                flag_driver = False
            else:
                flag_driver = True
            thread = Thread(
                target=yongshengzhihai.YongShengZhiHai().run, args=(n, flag_driver))
        elif self._choice == 3:
            # 3.业原火
            thread = Thread(target=yeyuanhuo.YeYuanHuo().run, args=(n,))
        elif self._choice == 4:
            # 4.御灵
            thread = Thread(target=yuling.YuLing().run, args=(n,))
        elif self._choice == 5:
            # 5.个人突破
            thread = Thread(target=jiejietupo.JieJieTuPoGeRen().run, args=(n,))
        elif self._choice == 6:
            # 6.寮突破
            thread = Thread(
                target=jiejietupo.JieJieTuPoYinYangLiao().run, args=(n,))
        elif self._choice == 7:
            # 7.道馆突破
            flag_guanzhan = self.ui.button_guanzhan.isChecked()
            thread = Thread(target=daoguantupo.DaoGuanTuPo().run,
                            args=(flag_guanzhan,))
        elif self._choice == 8:
            # 8.普通召唤
            thread = Thread(target=zhaohuan.ZhaoHuan().run, args=(n,))
        elif self._choice == 9:
            # 9.百鬼夜行
            thread = Thread(target=baiguiyexing.BaiGuiYeXing().run, args=(n,))
        elif self._choice == 10:
            # 10.限时活动
            thread = Thread(target=huodong.HuoDong().run, args=(n,))
        elif self._choice == 11:
            # 11.组队日轮副本
            # 是否司机（默认否）
            # 组队人数（默认2人）
            driver = self.ui.buttonGroup_driver.checkedButton().text()
            if driver == "否":
                flag_driver = False
            else:
                flag_driver = True
            flag_passengers = int(
                self.ui.buttonGroup_passengers.checkedButton().text())
            thread = Thread(
                target=rilun.RiLun().run,
                args=(n, flag_driver, flag_passengers)
            )

        # 线程存在
        if thread is not None:
            thread.daemon = True  # 线程守护
            thread.start()
        # 进行中
        self.is_fighting(True)

    def is_fighting(self, flag: bool):
        """程序是否运行中，启用/禁用其他控件"""
        if flag:
            self.ui.button_start.setText("进行中")
        else:
            self.ui.button_start.setText("开始")
        self.ui.combo_choice.setEnabled(not flag)
        self.ui.spinB_num.setEnabled(not flag)
        self.ui.button_start.setEnabled(not flag)
        # 御魂类小按钮
        self.ui.button_driver_False.setEnabled(not flag)
        self.ui.button_driver_True.setEnabled(not flag)
        self.ui.button_passengers_2.setEnabled(not flag)
        self.ui.button_passengers_3.setEnabled(not flag)

    def is_fighting_yuhun(self, flag: bool):
        """初始化组队御魂副本默认配置，显示/隐藏其他控件"""
        if flag:
            self.ui.label_driver.show()
            self.ui.button_driver_False.show()
            self.ui.button_driver_True.show()
            self.ui.label_passengers.show()
            self.ui.button_passengers_2.show()
            self.ui.button_passengers_3.show()
            self.ui.button_driver_False.setChecked(True)
            self.ui.button_passengers_2.setChecked(True)
        else:
            self.ui.label_driver.hide()
            self.ui.button_driver_False.hide()
            self.ui.button_driver_True.hide()
            self.ui.label_passengers.hide()
            self.ui.button_passengers_2.hide()
            self.ui.button_passengers_3.hide()

    # 关闭程序
    def closeEvent(self, event) -> None:
        try:
            log._write_to_file("[EXIT]")
        except:
            pass
        event.accept()
