#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
from utils.config import config
"""

from pathlib import Path
import yaml

from .mythread import MyThread


class Config():
    def __init__(self) -> None:
        self.version: str = "1.7.0"
        self.application_path: Path = Path.cwd()
        if Path(self.application_path / "resource").is_dir():
            self.resource_path: Path = self.application_path / "resource"
        else:
            self.resource_path: Path = self.application_path / "pic"
        print(self.resource_path)
        self.config_yaml_path: Path = self.application_path/"config.yaml"
        self.config_default: dict = {
            "更新模式": ["GitHub", "Gitee"],
            "悬赏封印": ["accept", "refuse", "ignore"]
        }

        thread_config_init = MyThread(func=self.config_yaml_init)
        thread_config_init.daemon = True
        thread_config_init.start()

    def config_yaml_init(self):
        if self.config_yaml_path.is_file():
            data = self.config_yaml_read()
            # 更新模式
            # self.update_mode = self.check_dict_key_is_in_list(
            #     data, "更新模式", ["GitHub", "Gitee"])
            # # 悬赏封印
            # self.xuanshangfengyin_receive = self.check_dict_key_is_in_list(
            #     data, "悬赏封印", ["accept", "refuse", "ignore"])
            data = self.check_config(data)
            print(self.xuanshangfengyin_receive)
        else:
            print("不存在配置文件")
            data = self.config_default
            for item in data.keys():
                value = data[item]
                if isinstance(value, list):
                    # data.pop(item)
                    # data.setdefault(item, value[0])
                    data[item]=value[0]
                else:
                    data[item]=value
        self.config_yaml_save(data)
        print("成功创建配置文件")

    def config_yaml_read(self) -> dict:
        with open(self.config_yaml_path, encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data

    def config_yaml_save(self, data):
        if isinstance(data, dict):
            with open(self.config_yaml_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False)
        else:
            print("保存失败")

    # def check_dict_key_is_in_list(self, config_dict: dict, key: str, config_list: list):
    #     """给出一个字典和键值，检查值是否包含在列表中，如包含，返回值；如未包含，返回列表第一个值

    #     Args:
    #         config_dict (dict): 待索引的字典
    #         key (str): 待查找的键值
    #         config_list (list): 需匹配的列表

    #     Returns:
    #         str: 匹配的值
    #     """
    #     if config_dict.get(key) in config_list:
    #         return config_dict.get(key)
    #     else:
    #         return config_list[0]

    def check_config(self, data: dict) -> dict:
        """检查配置字典的键值，返回符合配置要求的字典

        Args:
            data (dict): 待检查的字典

        Returns:
            dict: 符合配置要求的字典
        """
        data, self.update_mode = self.dict_set_default(data, "更新模式")
        data, self.xuanshangfengyin_receive = self.dict_set_default(
            data, "悬赏封印")
        return data

    def dict_set_default(self, data: dict, key: str) -> tuple[dict, str]:
        """检查字典的键值是否存在，并设置默认值

        Args:
            data (dict): 待检查的字典
            key (str): 待匹配的键值

        Returns:
            dict: 新字典
        """
        value = self.config_default.get(key)
        if isinstance(value, list):
            if not data.setdefault(key) in value:
                data.pop(key)
                data.setdefault(key, value[0])
        else:
            if data.setdefault(key) != value:
                data.pop(key)
                data.setdefault(key, value)
        return data, data.get(key)


config = Config()
