"""
log library
"""
# coding:utf-8

from typing import Any, Iterable, List, Mapping, TypeAlias
import requests
import base64
import uuid
import os
import hashlib
import pathlib
from tabulate import tabulate

from work_wechat_log.consts import MessageType, TableFmtType, TableHeadersType, TableType

"""
每个机器人发送的消息不能超过20条/分钟。
"""
class WorkWechatLog:
    headers = {"Content-Type": "text/plain"}

    def __init__(self, webhook_url: str, mode: bool = True) -> None:
        self.mode = mode
        self.webhook_url = webhook_url

    def post_message(self, data):
        """
        发送webhook请求
        """
        return requests.post(self.webhook_url, headers=self.headers, json=data).json()

    def text(self, msg: str, mentioned_list: List[str] = [], mentioned_mobile_list: List[str] = []):
        """
        文本内容，最长不超过2048个字节，必须是utf8编码
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": msg,
                "mentioned_list": mentioned_list,
                "mentioned_mobile_list": mentioned_mobile_list
            }
        }
        self.post_message(data)

    def tableformat(self, msg):
        # self.image(msg)
        print("暂未支持")

    def markdown(self, msg: str):
        """
        markdown内容，最长不超过4096个字节，必须是utf8编码
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": msg
            }
        }
        self.post_message(data)

    def image(self, image_path: str):
        with open(image_path, "rb") as image_file:
            image_base64 = str(base64.b64encode(
                image_file.read()), encoding='utf-8')
        image_md5 = hashlib.md5(pathlib.Path(
            image_path).read_bytes()).hexdigest()

        data = {
            "msgtype": "image",
            "image": {
                "base64": image_base64,
                "md5": image_md5
            }
        }
        self.post_message(data)

    def log(self, msg_type: str, msg: str):
        if self.mode:
            match msg_type:
                case MessageType.TEXT.value:
                    print(f"{msg}\n")
                    return
                case MessageType.MARKDOWN.value:
                    print(f"{msg}\n")
                    return
                case _:
                    print(f"开发模式不支持msg_type为 {msg_type} 的消息")
                    return
        else:
            match msg_type:
                case MessageType.TEXT.value:
                    return self.text(msg)
                case MessageType.MARKDOWN.value:
                    return self.markdown(msg)
                case MessageType.IMAGE.value:
                    return self.image(msg)
                case _:
                    return self.text(msg)

    def table(self, table: TableType, headers: TableHeadersType = (), tablefmt: TableFmtType = "simple"):
        table_value = tabulate(
            tabular_data=table, headers=headers, tablefmt=tablefmt)
        if self.mode:
            print(table_value)
        else:
            self.tableformat(table_value)
