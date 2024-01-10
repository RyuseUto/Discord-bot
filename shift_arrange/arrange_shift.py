import gspread
from oauth2client.service_account import ServiceAccountCredentials
from openpyxl import load_workbook
from googleapiclient.discovery import build
import re
import connect_spreadsheet as cs
import re

def exchange_time_row(in_time):
    # return int(intime) + 3
    return int(in_time) + 7

def extract_number_ranges(text):
    pattern = r'\d+-\d+'
    matches = re.finditer(pattern, text)
    range_matches = []
    non_range_matches = []

    last_end = 0

    for match in matches:
        start, end = match.span()
        if last_end < start:
            # [0-9]-[0-9]にマッチしない部分を取得
            non_match = text[last_end:start]
            non_range_matches.append(non_match)

        # [0-9]-[0-9]にマッチした部分を取得
        matched_range = text[start:end]
        range_matches.append(matched_range)
        last_end = end

    # 残りの非マッチ部分を取得
    remaining_text = text[last_end:]
    non_range_matches.append(remaining_text)

    return range_matches, non_range_matches

# 効率難易度表と検索する文字列を受け取り，検索結果を返す関数
def search_helper_organization(data, nickname):
    try:
        # 支援者の名前を表す列
        target_column_name = 0
        # 検索一致した行を保存する変数
        matching_rows = []
        
    
        # データを走査して文字列の先頭から一致する行を取得
        for row_index, row in enumerate(data):
            if row and len(row) > target_column_name and row[target_column_name] == nickname:
                matching_rows.append(row)

        # E, F, I, J, L, M 列のインデックス
        e_column_index = 4
        f_column_index = 5
        i_column_index = 8
        j_column_index = 9
        l_column_index = 11
        m_column_index = 12

        # E, F, I, J, L, M 列の値を保存する変数
        e_f_i_j_l_m_values_list = []

        # 対象行が見つかった場合、E, F, I, J, L, M 列の値を変数に保存
        if matching_rows:
            for row in matching_rows:
                e_f_i_j_l_m_values = [row[e_column_index], row[f_column_index], row[i_column_index], row[j_column_index], row[l_column_index], row[m_column_index]]
                e_f_i_j_l_m_values_list.append(e_f_i_j_l_m_values)

            
      
            return e_f_i_j_l_m_values_list
        else:
            null_data = ["","","","","",""]
            e_f_i_j_l_m_values_list.append(null_data)
            return e_f_i_j_l_m_values_list
    
    except Exception as e:
            print(f"効率難易度チャンネルエラー\n{e}")
            return "Error"


def get_helper_info(nickname):
    # スプレッドシート名（URLの一部）を指定
    spreadsheet_name = '支援編成いろいろ表'
    worksheet_name = '支援編成一覧'  # シート名
    helper_info = cs.connect_spreadsheet(spreadsheet_name, worksheet_name)
    helper_data = search_helper_organization(helper_info, nickname)
    return helper_data


def save_helper_shift(nickname, helper_data, file_name, content):

    # メッセージから入れるシフトの時間と，それ以外の条件メッセージを取得
    range_matches, non_range_matches = extract_number_ranges(content)

    # 入れる時間をさらに分割
    time_memo = []
    for i in range(0,len(range_matches)):
        time_se = []
        time_se = range_matches[i].split("-")
        time_memo.append(time_se)

    # シフト情報を取得
    # 認証情報JSONファイルのパスを指定
    credentials = ServiceAccountCredentials.from_json_keyfile_name('mytest.json', ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    # 認証情報を使用してGoogleスプレッドシートに接続
    gc = gspread.authorize(credentials)
    # スプレッドシート名（URLの一部）を指定
    spreadsheet_name = str(file_name)
    # スプレッドシートを開く
    sh = gc.open(spreadsheet_name)
    worksheet_name = 'シフト'  # シート名
    # シートを選択
    worksheet = sh.worksheet(worksheet_name)
    # シートからデータを読み込む
    shift_data = worksheet.get_all_values()
    shift_data = shift_data[2:]

    find_row = -1

    start_time = exchange_time_row(time_memo[0][0])
    end_time = exchange_time_row(time_memo[0][1])
    target_column_name = start_time
    is_break = False

    # まずはどこの行に挿入すれば良いのかを精査する
    for i in range(0, len(shift_data)):
        if shift_data[i][0] == '' or start_time == 7:
            print("in")
            find_row = i
            break
    
        for x in range(7, target_column_name):
            if shift_data[i][x] == "TRUE":
                break
            if x == (target_column_name - 1):
                find_row = i
                is_break = True
                break
    
        if is_break:
            break

    insert_row = find_row


    insert_data = [""] * 30  # リストを十分な要素数で初期化

    insert_data[0] = nickname

    insert_data[1:6] = helper_data[0]

    insert_data[7:30] = ["FALSE"] * 24  # "FALSE" を24回繰り返し

    insert_data[31] = ' '.join(non_range_matches)
 

    for i in range(0, len(time_memo)):
        start_time = exchange_time_row(time_memo[i][0])

        end_time = exchange_time_row(time_memo[i][1])
        if end_time > 32:
            end_time = 31

        for x in range(start_time, end_time):
            insert_data[x] = "TRUE"

    print(insert_data)

    # データを指定した位置に挿入
    shift_data.insert(insert_row, insert_data)

    range_end = len(shift_data) + 3

    # ワークシートに変更を反映
    worksheet.update(f"A3:AH{range_end}", shift_data, value_input_option='USER_ENTERED')

