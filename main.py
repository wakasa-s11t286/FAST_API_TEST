import datetime
import json
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, File, Form, UploadFile
from pydantic import BaseModel

from Services.CSVService import CSVService
from Services.SlackService import SlackService
from Services.Supabase.BusinessOfficeService import BusinessOfficeService
from Services.Supabase.StorageService import StorageService
from Services.Supabase.TransmissionFileService import (
    FileTableService,
    TransmissionFileService,
)

app = FastAPI()
load_dotenv()  # .envファイルから環境変数を読み込む


# リクエスト受け取るJSONの中身を定義
# TODO：API増えなければ消す(現状未使用)
class Info(BaseModel):
    business_office_num1: str = None
    business_office_num2: str = None
    sample: str = None

    # TODO:他にもあれば


@app.post("/uploadfile")
async def upload_file(info: str = Form(...), file: UploadFile = File(...)):
    # async def upload_file(info: Info = Depends(), file: UploadFile = File(...)):

    # async def upload_file(
    #    files: Annotated[
    #        list[UploadFile], File(description="Multiple files as UploadFile")
    #    ],
    # ):

    # # ストレージのバケット
    bucket_name = "FAXOCR"

    # 現在日時取得
    dt_now = datetime.datetime.now()
    dt_YM = dt_now.strftime("%Y%m")
    dt_YMDHMS = dt_now.strftime("%Y%m%d%H%M%S")

    # DB登録フラグ
    is_register = True
    file_list = []

    # 送信元/送信先 の事業所ID、事業所番号
    sender_id = None
    sender_business_office_num = None
    recieved_id = None
    recieved_business_office_num = None

    # JSONにマッピング
    json_data = json.loads(info)
    print("-------------リクエスト---------------")
    print(json_data)
    print(file.filename)

    # ファイルをバイト変換
    bytes_data = await file.read()
    # if f.content_type == "application/pdf":

    # JSONファイルの場合
    # JSON変換 UTF-8でくる想定（TODO もし違う場合、decode("文字コード"）する)
    # di = json.loads(bytes_data)

    # TODO：事業所名のキーの確認
    # 送信元 事業所
    sender_name = json_data["jigyosyo1"]
    # 送信先 事業所
    recieved_name = json_data["jigyosyo2"]

    # JSON → CSV作成
    temp_csv = CSVService.createCSV(json_data)
    # 作成したCSVデータをリストに追加
    file_data = {"type": "text/csv", "bytes": temp_csv}
    file_list.append(file_data)

    # 事業所名から事業所IDを取得する
    # 送信元の特定
    sender_info = BusinessOfficeService.getJigyosyoId(sender_name)
    if sender_info:
        sender_id = sender_info["id"]
        sender_business_office_num = sender_info["business_office_num"]

    # 送信先の特定
    recieved_info = BusinessOfficeService.getJigyosyoId(recieved_name)
    if recieved_info:
        recieved_id = recieved_info["id"]
        recieved_business_office_num = recieved_info["business_office_num"]

    if sender_id is None or recieved_id is None:
        # 送信元、または送信先の事業所IDが取得できない場合
        is_register = False

    # 受け取ったファイルをリストにつめる
    file_data = {"type": file.content_type, "bytes": bytes_data}
    file_list.append(file_data)

    if not is_register:
        # 宛先/差出不明の場合はSlack通知を送り、終了
        SlackService.unknownFileNotice(file_list)
        return {
            "result": {
                "is_register": is_register,
                "filename": file.filename,
                "送信元事業所名": sender_name,
                "送信先事業所名": recieved_name,
            }
        }

    # DB登録/ファイルアップロードを継続

    # csv_transmissonsの登録
    transmission_insert_id = TransmissionFileService.craeteRecord(
        sender=sender_id, recipient=recieved_id, message="FAXから送信されました"
    )

    # ストレージへの保管先
    file_path = sender_business_office_num + "/" + str(transmission_insert_id) + "/"
    # 拡張子を除くファイル名を作成
    file_name_temp = (
        "UPPLAN_"
        + dt_YM
        + "_"
        + sender_business_office_num
        + "_"
        + recieved_business_office_num
        + "_"
        + dt_YMDHMS
    )

    for f in file_list:
        # ファイルタイプごとにファイル名などを指定
        if f["type"] == "application/pdf":
            file_name = file_name_temp + ".pdf"
            file_label = "第6票(PDF)"
            content_type = "application/pdf"
            type = "pdf"

        elif f["type"] == "text/csv":
            file_name = file_name_temp + ".csv"
            file_label = "第6票(CSV)"
            content_type = "text/csv"
            type = "csv"
        else:
            # CSV、PDF以外はアップ及び登録はしない
            continue

        # ストレージアップロード
        StorageService.uploadFile(
            bucket=bucket_name,
            contentType=content_type,
            fileName=file_name,
            path=file_path,
            data=f["bytes"],
        )
        # csv_files登録
        FileTableService.craeteRecord(
            trans=transmission_insert_id,
            fileLabel=file_label,
            filePath=file_path + file_name,
            type=type,
        )

    return {
        "result": {
            "is_register": is_register,
            "filename": file.filename,
            "送信元事業所名": sender_name,
            "送信先事業所名": recieved_name,
        }
    }
