import json
import os

import httpx

from .application import VERSION, Connect
from .mysignal import global_ms as ms

__all__ = ["update_record", "get_update_info"]

UPDATE_INFO_FILE = "data/update_info.json"


def json_read(file_path: str):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def json_write(file_path: str, data: dict):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_update_info(_file):
    response = httpx.get(Connect.releases_api, headers=Connect.headers)
    if response.status_code != 200:
        return
    _api_data = json.loads(response.text)

    _list = []
    for i in range(5):
        _version = _api_data[i]["tag_name"][1:]
        _body = _api_data[i]["body"]
        _dict = {}
        _dict.setdefault("version", _version)
        _dict.setdefault("body", _body)
        _list.append(_dict)

    json_write(_file, _list)


def get_update_info():
    """获取更新记录"""
    if not os.path.exists("data"):
        os.mkdir("data")

    _update_file = UPDATE_INFO_FILE
    if os.path.exists(_update_file):
        _update_info = json_read(_update_file)
        if _update_info[0]["version"] == VERSION:
            return

    save_update_info(_update_file)


def update_record():
    """更新记录"""
    _update_info = json_read(UPDATE_INFO_FILE)
    for item in range(len(_update_info)):
        _version = _update_info[item].get("version")
        _body = _update_info[item].get("body")
        msg = f"{_version}\n{_body}\n"
        ms.update_record.text_update.emit(msg)
