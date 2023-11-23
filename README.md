# FAST_API_TEST
Python FAST APIのテストモジュール（Vercel上で動作させる）

## 環境構築


#### 前提
Pythonをインストールしてください。

#### 環境ファイルをコピー

プロジェクトディレクトリ直下のディレクトリで作業を行ってください。  
以下を実行し、.envを作成します。

```
cp .env.example .env
```

#### 環境変数の設定

.envの中身をSupabase環境、Slack環境に応じて編集します。  
以下はステージングの場合の変数(SLACKは開発用チャンネルを指定)

```
SUPABASE_URL="https://qjpvqsmzleoqcutndlwo.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFqcHZxc216bGVvcWN1dG5kbHdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTY4MTQ0MjcsImV4cCI6MjAxMjM5MDQyN30.ncQGGpyJXltnJ9mN13bAkqYHBYXGRy9qGOxpokW5cGc"
SLACK_TOKEN="xoxb-5718678533877-6227900106115-EvCM55BxxdTDOeakWfN7nNlF"
SLACK_CHANNEL="fax-ocr通知_テスト用"
```


### 関連モジュールのインストール
プロジェクトディレクトリ直下のディレクトリで作業を行ってください。  
以下を実行し、各種モジュールをインストールします。
```
pip install -r requirements.txt
```


### ローカルサーバで起動
プロジェクトディレクトリ直下のディレクトリで作業を行ってください。 
以下を実行し、ローカルサーバを起動します。  
(起動するPythonファイルによって、mainの箇所は変わります)
```
uvicorn main:app --reload
```  

停止する場合は、Ctrl + C

### APIの接続確認
APIリファレンス(Swagger)  

http://localhost:8000/docs#

  
各APIのエンドポイント  
http://localhost:8000/<作成時に指定したパス>


## 開発時の注意


#### 依存モジュールの追加
モジュールを追加した場合、「requirements.txt」に追記してください。

#### APIモジュールの追加
APIファイルを追加した場合、「vercel.json」をメンテナンスしてください。

