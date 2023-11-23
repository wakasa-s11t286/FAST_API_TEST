import os

from supabase import Client, create_client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(
    url,
    key,
)


class BusinessOfficeService:
    # 事業所名(マスタ)で事業所IDを検索して取得
    def getJigyosyoId(name, serviceType=None):
        response = (
            supabase.table("master_business_offices")
            .select("id, business_office_num, business_offices(id, fax_number)")
            .eq("business_office_name", name)
            .execute()
        )
        if not response.data or not response.data[0]["business_offices"]:
            # もし戻りが0件の場合(コミミ登録済み事業所ではない場合)、Noneを返す
            return None
        # 取得できた事業所IDと事業所番号を返却
        result = {
            "id": response.data[0]["business_offices"][0]["id"],
            "business_office_num": response.data[0]["business_office_num"],
        }
        # TODO：サービスタイプが不明の場合、複数取得できるためケアが必要
        return result
