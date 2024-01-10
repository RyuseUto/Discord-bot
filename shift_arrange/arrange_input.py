import re

#全角の数字を半角に変換する関数
def to_full_half(msg):
    for i in range(0,len(msg)):
        msg[i] = msg[i].replace('０', '0')
        msg[i] = msg[i].replace('１', '1')
        msg[i] = msg[i].replace('２', '2')
        msg[i] = msg[i].replace('３', '3')
        msg[i] = msg[i].replace('４', '4')
        msg[i] = msg[i].replace('５', '5')
        msg[i] = msg[i].replace('６', '6')
        msg[i] = msg[i].replace('７', '7')
        msg[i] = msg[i].replace('８', '8')
        msg[i] = msg[i].replace('９', '9')
    return msg

#全角の数字を半角に変換する関数
def to_full_half2(msg):
    hankaku_text = re.sub(r'[０-９]', lambda x: chr(ord(x.group(0)) - ord('０') + ord('0')), msg)
    return hankaku_text

#スペースを取り除き，カンマの種類を半角に統一する関数
def remove_space_and_change_commma(msg):
    msg = msg.replace(' ', '')
    msg = msg.replace('　', '')
    msg = msg.replace('\n', ',')
    msg = msg.replace('、', ',')
    msg = msg.replace('，', ',')
    return msg

def change_hyphen(msg):
    msg = msg.replace('~', '-')
    msg = msg.replace('〜', '-')
    msg = msg.replace('ー', '-')
    return msg
    

#絵文字に対応する時間帯を文字列で返す関数
def to_time(emoji):
    if emoji == '🇦':
        return '4-5'
    elif emoji == '🇧':
        return '5-6'
    elif emoji == '🇨':
        return '6-7'
    elif emoji == '🇩':
        return '7-8'
    elif emoji == '🇪':
        return '8-9'
    elif emoji == '🇫':
        return '9-10'
    elif emoji == '🇬':
        return '10-11'
    elif emoji == '🇭':
        return '11-12'
    elif emoji == '🇮':
        return '12-13'
    elif emoji == '🇯':
        return '13-14'
    elif emoji == '🇰':
        return '14-15'
    elif emoji == '🇱':
        return '15-16'
    elif emoji == '🇲':
        return '16-17'
    elif emoji == '🇳':
        return '17-18'
    elif emoji == '🇴':
        return '18-19'
    elif emoji == '🇵':
        return '19-20'
    elif emoji == '🇶':
        return '20-21'
    elif emoji == '🇷':
        return '21-22'
    elif emoji == '🇸':
        return '22-23'
    elif emoji == '🇹':
        return '23-24'
    elif emoji == ':regional_indicator_u:':
        return '24-25'
    elif emoji == ':regional_indicator_v:':
        return '25-26'
    elif emoji == ':regional_indicator_w:':
        return '26-27'
    elif emoji == ':regional_indicator_x:':
        return '27-28'
    else:
        return 'no_match'


#部屋番号を半角5or6文字に整形する関数
def make_room_number(msg):
    room_num = to_full_half2(msg)
    room_num = room_num.replace(';', '')
    channel_name = f'【{room_num}】部屋番号'
    return room_num, channel_name


def make_ebi_template(number, openings, my_skill, power, req_skill):
    send_msg = f"@null\nベテラン　エビ周回 \n部屋番号【{number}】　＠{openings}\n\n主：{my_skill}　{power}\n募：{req_skill}\n\nSF気にしないです〜\n#プロセカ募集　#プロセカ協力 "
    return send_msg

# 効率難易度表と検索する文字列を受け取り，検索結果を返す関数
def search_efficiency_and_return_arranged_result(data, keyword):
    
    try:
        # 曲名を表す列
        target_column_name = 0
        # 検索一致した行を保存する変数
        matching_rows = []
    
        # データを走査して文字列の先頭から一致する行を取得
        for row in data:
            if row and len(row) > target_column_name and row[target_column_name].startswith(keyword):
                matching_rows.append(row)

        # B列からF列の値を保存する変数
        b_to_f_values_list = []

        # 対象行が見つかった場合、B列からF列の値を変数に保存
        if matching_rows:
            for row in matching_rows:
                b_to_f_values = row[0:13] 
                b_to_f_values_list.append(b_to_f_values)
        
        return b_to_f_values_list
        
        
    
    except Exception as e:
            print(f"効率難易度検索エラー\n{e}")
            return None

# 効率難易度表と検索する文字列を受け取り，検索結果を返す関数
def search_and_return_music_result(data, keyword):
    
    try:
        # 曲名を表す列
        target_column_name = 0
        # 検索一致した行を保存する変数
        matching_rows = []
    
        # データを走査して文字列の先頭から一致する行を取得
        for row in data:
            if row and len(row) > target_column_name and row[target_column_name].startswith(keyword):
                matching_rows.append(row)

        # B列からF列の値を保存する変数
        b_to_f_values_list = []

        # 対象行が見つかった場合、B列からF列の値を変数に保存
        if matching_rows:
            for row in matching_rows:
                b_to_f_values = row[0] 
                b_to_f_values_list.append(b_to_f_values)
        
        return b_to_f_values_list
        
        
    
    except Exception as e:
            print(f"効率難易度検索エラー\n{e}")
            return None

def to_alpha(index):
    if 1 <= index <= 20:
        return chr(0x1F1E6 + index - 1)
    else:
        return '❌'  # マッチしない場合の絵文字




































"""
#絵文字に対応する時間帯を文字列で返す関数
def to_alpha(index):
    if index == 1:
        return '🇦'
         
    elif index == 2:
        return  '🇧'
         
    elif index == 3:
        return '🇨'
         
    elif index == 4:
        return '🇩'
         
    elif index == 5:
        return '🇪'
         
    elif index == 6:
        return '🇫'
 
    elif index == 7:
        return '🇬'

    elif index == 8:
        return '🇭'

    elif index == 9:
        return '🇮'
   
    elif index == 10:
        return '🇯'
  
    elif index == 11:
        return '🇰'

    elif index == 12:
        return '🇱'
     
    elif index == 13:
        return '🇲'

    elif index == 14:
        return '🇳'

    elif index == 15:
        return '🇴'

    elif index == 16:
        return '🇵'
     
    elif index == 17:
        return '🇶'

    elif index == 18:
        return '🇷'

    elif index == 19:
        return '🇸'
 
    elif index == 20:
        return '🇹'
        
    else:
         '❌'
"""