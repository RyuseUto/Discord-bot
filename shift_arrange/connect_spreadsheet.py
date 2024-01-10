import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_spreadsheet(spreadsheet_name, worksheet_name):
    try:
        # 認証情報JSONファイルのパスを指定
        credentials = ServiceAccountCredentials.from_json_keyfile_name('mytest.json', ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        # 認証情報を使用してGoogleスプレッドシートに接続
        gc = gspread.authorize(credentials)
        # スプレッドシートを開く
        sh = gc.open(spreadsheet_name)
        # シートを選択
        worksheet = sh.worksheet(worksheet_name)
        # シートからデータを読み込む
        mydata = worksheet.get_all_values()
        return mydata
    except Exception as e:
            print(f"チャンネル取得エラー\n{e}")
            return None