#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tansuo.py
"""探索副本-单人-暂且"""

import time
from pathlib import Path

import pyautogui

from ..utils.application import RESOURCE_DIR_PATH
from ..utils.coordinate import Coor
from ..utils.decorator import log_function_call, run_in_thread, time_count
from ..utils.function import (
    check_click,
    check_finish_once,
    check_scene,
    check_scene_multiple_once,
    click,
    finish_random_left_right,
    get_coor_info,
    image_file_format,
    random_sleep
)
from ..utils.log import log
from ..utils.window import window


# class TanSuo:
#     """探索副本-单人-暂且"""

#     @log_function_call
#     def __init__(self) -> None:
#         self.scene_name: str = "探索副本-单人"
#         self.resource_path: str = "tansuo"  # 图片路径
#         self.m: int = 0  # 当前次数

#     def title(self) -> bool:
#         """场景"""
#         flag_title = True  # 场景提示
#         while True:
#             if function.judge_scene(f"{self.resource_path}/tansuo_28_title.png", "探索28章"):
#                 return True
#             elif function.judge_scene(f"{self.resource_path}/tansuo_28.png", "探索"):
#                 log.warn("请检查游戏场景", True)

#     def judge_scene_tansuo(self):
#         """场景判断"""
#         scene = {
#             "tansuo_28_title.png": "少女与面具",
#             "chuzhanxiaohao.png": "出战消耗"
#         }
#         for item in scene.keys():
#             x, y = function.get_coor_info_picture(
#                 f"{self.resource_path}/{item}")
#             if x != 0 and y != 0:
#                 return scene[item]

#     def judge_scene_tansuo_is_kunnan(self):
#         """是否困难模式"""
#         while True:
#             if function.judge_scene(f"{self.resource_path}/kunnan_big.png", "困难"):
#                 return True
#             else:
#                 time.sleep(1)
#                 function.judge_click(f"{self.resource_path}/putong_small.png")
#                 time.sleep(1)

#     def judge_scene_tansuo_is_auto(self):
#         """是否自动轮换"""
#         while True:
#             if function.judge_scene(f"{self.resource_path}/zidonglunhuan.png"):
#                 return True
#             else:
#                 log.warn("请自行设置并打开 自动轮换 功能", True)

#     def get_coor_info_tansuo_center(self, file: str):
#         """
#         图像识别，返回匹配到的第一个图像的中心坐标

#         参数:
#         file (Path | str): 图像名称

#         返回:
#             Coor: 识别成功，返回匹配到的第一个图像的中心坐标，识别识别，返回(0,0)
#         """
#         # filename: str = fr"./pic/{self.picpath}/{pic}"
#         filename = self.resource_path / file
#         log.info(filename)
#         if isinstance(filename, Path):
#             filename = str(filename)
#         try:
#             button_location = pyautogui.locateOnScreen(
#                 filename,
## region=(
#                     window.window_left,
#                     window.window_top,
#                     window.absolute_window_width,
#                     window.absolute_window_height
#                 ),
#                 confidence=0.8
#             )
#         except Exception:
#             pass

#     @run_in_thread
#     @time_count
#     @log_function_call
#     def run(self):
#         time.sleep(2)
#         if self.title():
#             log.num(f"0/{self.n}")
#             function.random_sleep(1, 3)
#             while self.m < self.n:
#                 time.sleep(1)
#                 if self.judge_scene_tansuo_is_kunnan():
#                     function.judge_click(f"{self.resource_path}/tansuo.png")
#                     if self.judge_scene_tansuo_is_auto():
#                         pass

#         text = f"已完成 探索困难28章 {self.m}次"
#         log.info(text, True)


class TanSuo:
    """探索"""
    scene_name = "探索"
    resource_path = "tansuo"
    resource_list: list = [
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
        "treasure_box",
        "zidonglunhuan"
    ]

    def __init__(self, n: int = 0) -> None:
        self.n = 0  # 当前次数
        self.max = n  # 总次数
        self.flag_done_once: bool = False

    def get_all_coor_info_tansuo_center(self, file: str):
        """图像识别，返回匹配到的第一个图像的中心坐标

        参数:
            file (Path | str): 图像名称

        用法：
            `filename`

        返回:
            Coor: 识别成功，返回匹配到的第一个图像的全局中心坐标，识别失败，返回(0,0)
        """
        _file_name = image_file_format(RESOURCE_DIR_PATH / self.resource_path / file)
        log.info(_file_name)
        try:
            for button_location in pyautogui.locateAllOnScreen(
                _file_name,
                region=(
                    window.window_left,
                    window.window_top,
                    window.absolute_window_width,
                    window.absolute_window_height
                ),
                confidence=0.8
            ):
                log.info(f"button_location: {button_location}")
                button_location_center = pyautogui.center(button_location)
                log.info(f"button_location_center: {button_location_center}")
                return Coor(button_location_center.x, button_location_center.y)
            # 未匹配到一个
            return Coor(0, 0)
        except Exception:
            return Coor(0, 0)

    def title_single(self) -> bool:
        """场景"""
        flag_title = True  # 场景提示
        while True:
            if check_scene(f"{self.resource_path}/title.png", self.scene_name):
                return True
            elif flag_title:
                flag_title = False
                log.warn("请检查游戏场景", True)

    def title_daoguan(self) -> bool:
        """场景"""
        flag_title = True  # 场景提示
        self.flag_fighting = False  # 进行中
        flag_daojishi = True  # 倒计时
        while True:
            if check_scene(f"{self.resource_path}/title.png", self.scene_name):
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

    @log_function_call
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
            scene, coor = check_scene_multiple_once(scene_list, self.resource_path)
            if scene is None:
                continue
            if "/" in scene:
                scene = scene.split("/")[-1]
            log.info(f"当前场景: {scene}")

            match scene:
                case "chuzhanxiaohao" | "tansuo_28" | "tansuo_28_0" | "tansuo_28_title":
                    return True
                case _:
                    if flag_title:
                        flag_title = False
                        log.warn("请检查游戏场景", True)

    @log_function_call
    def fighting(self):
        _flag: bool = False
        while True:
            if check_finish_once():
                _flag = True
                random_sleep(0.5, 0.8)
                finish_random_left_right()
            elif _flag:
                self.flag_done_once = True
                return
            random_sleep(1, 1.5)

    @log_function_call
    def finish(self):
        """boss战后的结束阶段

        1.有掉落物，不需要点击，直接左上角退出即可
        2.无掉落物，系统自动跳转出去
        3.1、2出来之后，存在宝箱/妖气封印的可能，当前章节的小界面被关闭，需要右侧列表重新点开
        """
        # 等待加载完毕
        random_sleep(1.5, 2)
        coor = get_coor_info(f"{self.resource_path}/chuzhanxiaohao")
        if coor.is_effective:
            check_click(f"{self.resource_path}/quit")
            random_sleep(0.4, 0.8)
            check_click(f"{self.resource_path}/quit_true")
        else:
            coor = get_coor_info(f"{self.resource_path}/tansuo")
            # 宝箱
            if coor.is_zero:
                coor_2 = get_coor_info(f"{self.resource_path}/treasure_box")
                if coor_2.is_effective:
                    click(coor_2)
                    random_sleep(1.5, 2)
                    click()
                    return

    @run_in_thread
    @time_count
    @log_function_call
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
                function.random_finish_left_right(is_multiple_drops_y=True)
                function.random_sleep(1, 3)
                self.n += 1
                log.num(f"{self.n}/{self.max}")
        text = f"已完成 {self.scene_name} {self.n}次"
        log.ui(text)

    @run_in_thread
    @time_count
    @log_function_call
    def run(self):
        log.ui("单人探索，测试功能，未完成")
        self.max = 2
        while self.n < self.max and self.title():
            _scene_list = [
                "tansuo_28_0",
                "tansuo_28_title",
                "kunnan_big",
                "tansuo",
                "chuzhanxiaohao",
            ]
            scene, coor = check_scene_multiple_once(_scene_list, self.resource_path)
            if scene is None:
                continue
            if "/" in scene:
                scene = scene.split("/")[-1]
            log.info(f"当前场景: {scene}")

            match scene:
                case "tansuo_28_0":  # 右侧列表按钮
                    # function.judge_click(f"{self.resource_path}/tansuo")
                    click(coor)
                    random_sleep(1, 2)
                    # self.n += 1
                case "tansuo_28_title":
                    check_click(f"{self.resource_path}/tansuo")
                    # self.n += 1
                    random_sleep(2, 3)
                case "chuzhanxiaohao":
                    random_sleep(0.5, 1)
                    # 先判断boss面灵气
                    coor = get_coor_info(f"{self.resource_path}/fighting_boss")
                    if coor.is_effective:
                        click(coor)
                        self.fighting()
                    else:
                        coor = self.get_all_coor_info_tansuo_center("fighting")
                        if coor.is_effective:
                            click(coor)
                            self.fighting()
                    random_sleep(1, 2)
                    if self.flag_done_once:
                        self.finish()
