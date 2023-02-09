#!/usr/bin/env python3
# tansuo.py
"""
探索副本-单人-暂且
"""

from pathlib import Path
import time
import pyautogui

from utils.window import window
from utils.function import function
from utils.log import log

"""
探索困难28场景
tansuo_28_title.png
"""


class TanSuo:
    """探索副本-单人-暂且"""

    def __init__(self) -> None:
        self.scene_name: str = "探索副本-单人"
        self.resource_path: str = "tansuo"  # 图片路径
        self.m: int = 0  # 当前次数

    def title(self) -> bool:
        """场景"""
        flag_title = True  # 场景提示
        while True:
            if function.judge_scene(f"{self.resource_path}/tansuo_28_title.png", "探索28章"):
                return True
            elif function.judge_scene(f"{self.resource_path}/tansuo_28.png", "探索"):
                log.warn("请检查游戏场景", True)

    def judge_scene_tansuo(self):
        """场景判断"""
        scene = {
            "tansuo_28_title.png": "少女与面具",
            "chuzhanxiaohao.png": "出战消耗"
        }
        for item in scene.keys():
            x, y = function.get_coor_info_picture(
                f"{self.resource_path}/{item}")
            if x != 0 and y != 0:
                return scene[item]

    def judge_scene_tansuo_is_kunnan(self):
        """是否困难模式"""
        while True:
            if function.judge_scene(f"{self.resource_path}/kunnan_big.png", "困难"):
                return True
            else:
                time.sleep(1)
                function.judge_click(f"{self.resource_path}/putong_small.png")
                time.sleep(1)

    def judge_scene_tansuo_is_auto(self):
        """是否自动轮换"""
        while True:
            if function.judge_scene(f"{self.resource_path}/zidonglunhuan.png"):
                return True
            else:
                log.warn("请自行设置并打开 自动轮换 功能", True)

    def get_coor_info_picture_tansuo_center(self, file: str):
        """
        图像识别，返回匹配到的第一个图像的中心坐标

        :param pic: 文件路径&图像名称(*.png)
        :return: 识别成功，返回匹配到的第一个图像的中心坐标，识别识别，返回(0,0)
        """
        # filename: str = fr"./pic/{self.picpath}/{pic}"
        filename = self.resource_path / file
        log.info(filename)
        if isinstance(filename, Path):
            filename = str(filename)
        try:
            button_location = pyautogui.locateOnScreen(
                filename,
                region=(
                    window.window_left,
                    window.window_top,
                    window.absolute_window_width,
                    window.absolute_window_height
                ),
                confidence=0.8
            )
        except:
            pass

    def run(self):
        time.sleep(2)
        time_progarm = function.TimeProgram()  # 程序计时
        time_progarm.start()
        if self.title():
            log.num(f"0/{self.n}")
            function.random_sleep(1, 3)
            while self.m < self.n:
                time.sleep(1)
                if self.judge_scene_tansuo_is_kunnan():
                    function.judge_click(f"{self.resource_path}/tansuo.png")
                    if self.judge_scene_tansuo_is_auto():
                        pass

        text = f"已完成 探索困难28章 {self.m}次"
        time_progarm.end()
        text = text + " " + time_progarm.print()
        log.info(text, True)
        # 启用按钮
        log.is_fighting(False)
