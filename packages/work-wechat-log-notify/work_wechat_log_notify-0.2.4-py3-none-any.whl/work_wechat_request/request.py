"""
Work wechat 请求模块
"""
from typing import List
import requests
import time

from work_wechat_request.consts import WebhookUrls


class WorkWechatRequest:
    _instance = None

    @classmethod
    def get_instance(cls, webhook_urls: List[str]):
        dics = list(map(lambda url: {"url": url, "timestamp": 0}, webhook_urls))
        if cls._instance is not None and cls._instance.webhook_urls == dics:
            return cls._instance
        else:
            cls._instance = WorkWechatRequest(dics)
            return cls._instance

    def __init__(self, webhook_urls: WebhookUrls) -> None:
        self.webhook_urls = webhook_urls
        print(webhook_urls)
        self.headers = {"Content-Type": "text/plain"}
        self.retry = 0

    def _get_webhook_url(self) -> str:
        return next((dicitem["url"] for dicitem in self.webhook_urls if dicitem["timestamp"] < time.time()), "")
    
    def _set_delay_webhook_url(self, webhook_url: str):
        for item in self.webhook_urls:
            if item["url"] == webhook_url:
                item["timestamp"] = time.time() + 65

    def post_file(self, file_path: str):
        """
        发送文件请求
        """
        webhook_url = self._get_webhook_url()
        if webhook_url == "" and self.retry > 3:
            raise "没有符合要求的webhook_url"
        elif webhook_url == "":
            self.retry += 1
            self._set_delay_webhook_url(webhook_url)
            time.sleep(60)
            return self.post_file(file_path)
        else:
            return requests.post(webhook_url.replace("send", "upload_media") + "&type=file", files=[("media", open(file_path, "rb"))]).json()

    def post_message(self, data):
        """
        发送webhook请求
        """
        webhook_url = self._get_webhook_url()
        if webhook_url == "" and self.retry > 3:
            raise "没有符合要求的webhook_url"
        elif webhook_url == "":
            self.retry += 1
            self._set_delay_webhook_url(webhook_url)
            time.sleep(60)
            return self.post_message(data)
        else:
            if requests.post(webhook_url, headers=self.headers, json=data).ok:
                self.retry = 0
            else:
                if self.retry <= 3:
                    self.retry += 1
                    return self.post_message(data)
                else:
                    raise "重试3次, 未找到符合要求的webhook_url"
