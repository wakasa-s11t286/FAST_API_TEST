import os

from supabase import Client, create_client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(
    url,
    key,
)


class StorageService:
    def uploadFile(fileName=None, path=None, contentType=None, data=None, bucket=None):
        supabase.storage.from_(bucket).upload(
            file=data,
            path=path + "/" + fileName,  # ストレージに保管するときのパス及びファイル名を指定
            file_options={"content-type": contentType},
        )
