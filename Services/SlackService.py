import os

import requests

TOKEN = os.environ.get("SLACK_TOKEN")
CHANNEL = os.environ.get("SLACK_CHANNEL")

CHAT_URL = os.environ.get("SLACK_CHAT_URL")
UPLOAD_URL = os.environ.get("SLACK_UPLOAD_URL")



class SlackService:
    # メッセージの送信
    @staticmethod
    def chatMessage(text):
        headers = {"Authorization": "Bearer " + TOKEN}
        data = {"channel": CHANNEL, "text": text}
        requests.post(CHAT_URL, headers=headers, data=data)

    # ファイルアップロード
    @staticmethod
    def fileUpload(title=None, fileName=None, bytes=None, fileType=None):
        files = {
            "file": (fileName, bytes, "text/tab-separated-values"),
        }
        data = {
            "token": TOKEN,
            "channels": CHANNEL,
            "title": title,
            "filename": fileName,
            "filetype": fileType,
        }
        requests.post(
            UPLOAD_URL,
            data=data,
            files=files,
        )

    # 宛先、差出不明のfaxを通知
    def unknownFileNotice(files):
        # メッセージの送信
        text = "送信先または送信元が不明のFaxを受信しました。"
        SlackService.chatMessage(text)

        # ファイルアップロード
        for f in files:
            if f["type"] == "application/json":
                file_name = "Fax-OCR"
                file_type = "json"
                title = "OCR解析した連携ファイル"
            elif f["type"] == "text/csv":
                file_name = "Fax to CSV"
                file_type = "csv"
                title = "OCR解析したCSVファイル"

            else:
                file_name = "Fax-Data"
                file_type = "pdf"
                title = "FAXをPDFにしたもの"
            SlackService.fileUpload(
                title=title, fileName=file_name, bytes=f["bytes"], fileType=file_type
            )
