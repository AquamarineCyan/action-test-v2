#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tansuo.py
"""
探索副本-单人-暂且
"""

from pathlib import Path
import time
import pyautogui


from utils.function import function, time_consumption_statistics
from utils.log import log
from utils.window import window
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

    @ time_consumption_statistics
    def run(self):
        time.sleep(2)
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
        log.info(text, True)


class TanSuoTest:
    """探索 test"""

    def __init__(self, n: int = 0) -> None:
        self.scene_name = "探索"
        self.resource_path = "tansuo"  # 路径
        self.n = 0  # 当前次数
        self.max = n  # 总次数
        self.scene_list: list = [
            "boss_finish",
            "chuzhanxiaohao",
            "fighting",
            "fighting_boss",
            "kunnan_big",
            "kunnan_small",
            "putong_big",
            "putong_small",
            "quit_true",
            "quit_true_false",
            "tansuo",
            "tansuo_28",
            "tansuo_28_0",
            "tansuo_28_title",
            "treasure_chest",
            "zidonglunhuan"
        ]

    def title_simple(self) -> bool:
        """场景"""
        flag_title = True  # 场景提示
        while True:
            if function.judge_scene(f"{self.resource_path}/title.png", self.scene_name):
                return True
            elif flag_title:
                flag_title = False
                log.warn("请检查游戏场景", True)

    def judge_scene_daoguantupo(self) -> str:
        """场景判断"""
        scene = {
            "daojishi.png": "倒计时",
            "shengyutuposhijian.png": "可进攻",
            "guanzhuzhan.png": "馆主战",
            "button_zhuwei.png": "进行中"
        }  # "可进攻"未实现
        for item in scene.keys():
            x, y = self.get_coor_info_picture(item)
            if x != 0 and y != 0:
                return scene[item]

    def title_daoguan(self) -> bool:
        """场景"""
        flag_title = True  # 场景提示
        self.flag_fighting = False  # 进行中
        flag_daojishi = True  # 倒计时
        while True:
            if function.judge_scene(f"{self.resource_path}/title.png", self.scene_name):
                while True:
                    # 等待倒计时自动进入
                    if self.judge_scene_daoguantupo() == "倒计时":
                        if flag_daojishi:
                            log.info("等待倒计时自动进入", True)
                            flag_daojishi = False
                        self.flag_fighting = True
                        break
                    elif self.judge_scene_daoguantupo() == "可进攻":
                        self.flag_fighting = False
                        break
                    # 馆主战
                    elif self.judge_scene_daoguantupo() == "馆主战":
                        log.warn("待开发", True)
                        break
                return True
            # 已进入道馆进攻状态
            elif self.judge_scene_daoguantupo() == "进行中":
                log.info("道馆突破进行中", True)
                self.flag_fighting = True
                return True
            elif flag_title:
                flag_title = False
                log.warn("请检查游戏场景", True)

    def title(self) -> bool:
        flag_title = True  # 场景提示
        flag_fighting = False  # 进行中
        while True:
            scene_list: list = [
                "chuzhanxiaohao",
                "tansuo_28",
                "tansuo_28_0",
                "tansuo_28_title"
            ]
            scene = function.check_scene_multiple_once(scene_list)
            match scene:
                case "chuzhanxiaohao":
                    log.ui("chuzhanxiaohao")
                    return True
                case "tansuo_28":
                    log.ui("tansuo_28")
                    return True
                case "tansuo_28_0":
                    log.ui("tansuo_28_0")
                    return True
                case "tansuo_28_title":
                    log.ui("tansuo_28_title")
                    return True
                case _:
                    if flag_title:
                        flag_title = False
                        log.warn("请检查游戏场景", True)

    @time_consumption_statistics
    def run_0(self) -> None:
        time.sleep(2)
        if self.title():
            log.num(f"0/{self.max}")
            function.random_sleep(1, 3)
            while self.n < self.max:
                function.random_sleep(1, 2)
                # 开始
                function.judge_click(f"{self.resource_path}/tiaozhan.png")
                # 结束
                function.result()
                function.random_sleep(1, 2)
                # 结算
                function.random_finish_left_right(is_yuling=True)
                function.random_sleep(1, 3)
                self.n += 1
                log.num(f"{self.n}/{self.max}")
        text = f"已完成 {self.scene_name} {self.n}次"
        log.ui(text)

    @time_consumption_statistics
    def run(self):
        log.ui("单人探索，测试功能，未完成")
        self.max = 2
        while self.n < self.max and self.title():
            scene_list = [
                "tansuo_28_0",
                "tansuo_28_title",
                "kunnan_big",
                "tansuo"
            ]
            while True:
                scene, (x, y) = function.check_scene_multiple_once(scene_list, self.resource_path)
                if x != 0 and y != 0:
                    log.scene(scene)
                    log.ui("complete")
                    break
            match scene:
                case "tansuo_28_0":
                    # function.judge_click(f"{self.resource_path}/tansuo")
                    function.click(x, y)
                    self.n += 1
                    time.sleep(2)
                case "tansuo_28_title":
                    function.judge_click(f"{self.resource_path}/tansuo")
                    self.n += 1
