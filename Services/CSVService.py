import io

import pandas as pd


class CSVService:
    # JSONからインメモリ上にCSVを作成し、Bytesデータを返す
    def createCSV(ocr):
        # TODO：がんばってCSVを組み立てる

        csv_string = '居宅介護支援事業者事業所名,サービス事業者事業所名\r\n'
        csv_string += f'{ocr.fields["居宅介護支援事業者事業所名"].content},{ocr.fields["予実管理表（タイトル）"].value[0].value["サービス事業者事業所名"].content}\r\n'

        # UTF8へエンコード
        csv_binary = csv_string.encode("utf-8")
        # ByteIOへ変換
        temp_file_object = io.BytesIO(csv_binary)
        return temp_file_object.read()
