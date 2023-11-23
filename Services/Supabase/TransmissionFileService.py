import datetime
import os

import pandas as pd
from supabase import Client, create_client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(
    url,
    key,
)


class TransmissionFileService:
    # csv_transmissionsに新規レコードを作成
    def craeteRecord(sender=None, recipient=None, message=""):
        # 現在日時取得
        dt_now = datetime.datetime.now()
        timestamp = str(pd.Timestamp(dt_now, tz="Asia/Tokyo"))
        status = "Unsent"

        response = (
            supabase.table("csv_transmissions")
            .insert(
                {
                    "sender_id": sender,
                    "recipient_id": recipient,
                    "message": message,
                    "created_at": timestamp,
                    "sent_at": timestamp,
                    "status": status,
                    # TODO "source":"fax",
                }
            )
            .execute()
        )
        # 新規登録で採番したIDを返す
        return response.data[0]["id"]


class FileTableService:
    # csv_filesに新規レコードを作成
    def craeteRecord(trans=None, filePath=None, fileLabel="", type=None):
        response = (
            supabase.table("csv_files")
            .insert(
                {
                    "trans_id": trans,
                    "file_label": fileLabel,
                    "file_path": filePath,
                    # TODO "type":type,
                }
            )
            .execute()
        )
        # 新規登録で採番したIDを返す
        return response.data[0]["id"]
