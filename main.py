import os
import shutil
import tempfile
from pathlib import Path

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
async def upload_file(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, dir=".", suffix=".pdf") as temp_file:
        # リクエストされたファイルを一時保管（なせdelete=Trueだと権限エラーになる）
        shutil.copyfileobj(file.file, temp_file)
        tmp_path = Path(temp_file.name)

        # 一時保管したファイルをsupabaseへアップロードする
        with open(tmp_path, "rb") as f:
            supabase.storage.from_(bucket_name).upload(
                file=f,
                path="/" + file.filename,  # ストレージに保管するときのパス及びファイル名を指定
                file_options={"content-type": "application/pdf"},
            )

    # 一時保管したファイルを削除
    os.remove(tmp_path)

    # TODO：何かDB登録が必要であれば記述

    return {"filename": file.filename}
