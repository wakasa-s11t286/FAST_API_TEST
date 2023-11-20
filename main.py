import datetime
import os
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from supabase import Client, create_client

app = FastAPI()
load_dotenv()  # .envファイルから環境変数を読み込む

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(
    url,
    key,
)
bucket_name = "FAXOCR"


# リクエスト受け取るJSONの中身を定義
class Info(BaseModel):
    business_office_num: str
    file_name: int
    # TODO:他にもあれば


@app.get("/")
async def root():
    return {"greeting": "Hello world"}


@app.post("/create")
async def create_fax_data(info: Info):
    # TODO：サンプル
    # リファレンス： https://supabase.com/docs/reference/python/insert
    data, count = (
        supabase.table("csv_files")
        .insert({"trans_id": info.business_office_num, "file_label": info.file_name})
        .execute()
    )
    return {"status": "OK"}


@app.post("/uploadfile")
async def upload_file(file: Annotated[bytes, File()]):
    # 現在日時取得
    dt_now = datetime.datetime.now()
    # 現在日時からファイル名作成
    filename = dt_now.strftime("%Y%m%d%H%M%S")
    # supabaseへアップロードする
    supabase.storage.from_(bucket_name).upload(
        file=file,
        path="/" + filename + ".pdf",  # ストレージに保管するときのパス及びファイル名を指定
        file_options={"content-type": "application/pdf"},
    )

    return {"filename": filename}
