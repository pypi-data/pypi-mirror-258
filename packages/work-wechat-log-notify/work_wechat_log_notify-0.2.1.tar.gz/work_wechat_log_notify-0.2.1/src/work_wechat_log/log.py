"""
log library
"""
# coding:utf-8

from typing import List
import base64
import uuid
import hashlib
import pathlib
from tabulate import tabulate
import tempfile
import matplotlib.pyplot as plt

from work_wechat_log.consts import TableFmtType, TableHeadersType, TableType
from work_wechat_request.request import WorkWechatRequest

"""
每个机器人发送的消息不能超过20条/分钟。
"""
class WorkWechatLog:
    headers = {"Content-Type": "text/plain"}

    def __init__(self, webhook_urls: str | List[str], mode: bool = True) -> None:
        self.mode = mode

        if isinstance(webhook_urls, str):
            urls = [webhook_urls]
        else:
            urls = webhook_urls

        self.request = WorkWechatRequest.get_instance(urls)

    def text(self, msg: str, mentioned_list: List[str] = [], mentioned_mobile_list: List[str] = []):
        """发送文本消息

        Parameters
        ----------
        msg : str
            文本内容，最长不超过2048个字节，必须是utf8编码

        mentioned_list: List[str]
            userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
        
        mentioned_mobile_list: List[str]
            手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人

        Returns
        -------
        None
        """
        if self.mode:
            print(msg)
            return True

        data = {
            "msgtype": "text",
            "text": {
                "content": msg,
                "mentioned_list": mentioned_list,
                "mentioned_mobile_list": mentioned_mobile_list
            }
        }
        self.request.post_message(data)

    def markdown(self, msg: str):
        """发送markdown消息
        Parameters
        ----------
        msg : str
            markdown内容，最长不超过4096个字节，必须是utf8编码

        Returns
        -------
        None
        """
        if self.mode:
            print(msg)
            return

        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": msg
            }
        }
        self.request.post_message(data)

    def image(self, image_path: str):
        """发送图片消息

        Parameters
        ----------
        image_path : str
            图片地址

        Returns
        -------
        None
        """
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
        self.request.post_message(data)

    def table(self, table: TableType, headers: TableHeadersType = (), tablefmt: TableFmtType = "simple"):
        """发送表格消息

        Parameters
        ----------
        see: https://pypi.org/project/tabulate/

        Returns
        -------
        None
        """
        table_value = tabulate(
            tabular_data=table, headers=headers, tablefmt=tablefmt)
        if self.mode:
            print(table_value)
        else:
            # 创建一个plot
            _, _ = plt.subplots()
            plt.axis('off')
            # 在plot上添加text
            plt.text(0.4, 0.5, table_value, horizontalalignment='center', verticalalignment='center')
            # 保存图片
            with tempfile.TemporaryDirectory() as tempdir:
                image_path = f"{tempdir}/{uuid.uuid4()}.png"
                # 保存图像到临时目录
                plt.savefig(image_path)
                self.image(image_path)
