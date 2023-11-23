import io

import pandas as pd


class CSVService:
    # JSONからインメモリ上にCSVを作成し、Bytesデータを返す
    def createCSV(json):
        df_json = pd.json_normalize(json)
        # JSONをCSV形式の文字列へ
        # TODO：加工がいる場合、修正する
        csv_string = df_json.to_csv(header=True, index=False)

        # UTF8へエンコード
        csv_binary = csv_string.encode("utf-8")
        # ByteIOへ変換
        temp_file_object = io.BytesIO(csv_binary)
        return temp_file_object.read()
