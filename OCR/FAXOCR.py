import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

# Azure Form Recognizerの情報
URL = os.environ.get("AZURE_OCR_URL")
KEY = os.environ.get("AZURE_OCR_KEY")

class FAXOCR:

    def analyticsPDF(data):
        
        # モデルIDとドキュメントのパス
        model_id = "FAXOCR"

        # クライアントの作成
        document_analysis_client = DocumentAnalysisClient(
            endpoint=URL, credential=AzureKeyCredential(KEY)
        )

        # ドキュメントを読み込みAPI実行
        print("------------------OCR読み込み開始------------------")
        poller = document_analysis_client.begin_analyze_document(model_id, data)
        #with open(Document_Path, "rb") as f:
        #    poller = document_analysis_client.begin_analyze_document(model_id, f)
        print("------------------OCR結果出力------------------")
        result = poller.result()

        # 結果の表示
        print(f'保険者番号：{result.documents[0].fields["保険者番号"].content}')
        print(f'被保険者番号：{result.documents[0].fields["被保険者番号"].content}')
        print(f'保険者名：{result.documents[0].fields["保険者名"].content}')
        print(f'居宅介護支援事業者事業所名：{result.documents[0].fields["居宅介護支援事業者事業所名"].content}')
        print(f'担当者：{result.documents[0].fields["担当者"].content}')
        print(f'作成年月日：{result.documents[0].fields["作成年月日"].content}')
        print(f'生年月日：{result.documents[0].fields["生年月日"].content}')
        print(f'対象年月日：{result.documents[0].fields["対象年月日"].content}')
        print(f'前月までの短期入所利用日数：{result.documents[0].fields["前月までの短期入所利用日数"].content}')
        # print(f'予実管理表（タイトル）：{result.documents[0].fields["予実管理表（タイトル）"].content}')
        # print(f'予実管理表（予実）：{result.documents[0].fields["予実管理表（予実）"].content}')

        return result