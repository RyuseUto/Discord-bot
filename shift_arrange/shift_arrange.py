import discord
import numpy as np
import pandas as pd
from discord.ext import tasks
import arrange_input as arr
import connect_spreadsheet as cs
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import arrange_shift as AS

TOKEN = "mytoken"
SERVER_ID = 0

channel_list = {}
custom_emoji_id = 0  # カスタム絵文字のID
custom_emoji_name = 'name'
all_messages = []


# 接続に必要なオブジェクトを生成
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():

    global efficiency_difficulty_level_data
    global remind_list
    print("シフト書き込みシステムに接続しました！")


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):

    global SERVER_ID
    global channel_list
    global custom_emoji_id
    global custom_emoji_name

    # メッセージ送信者がBotだった場合は無視する
    if not message.author.bot and message.guild.id == SERVER_ID:
        try:
            # メッセージを標準形式に変換
            # これで　空行の削除，数字の半角化，ハイフンの - への統一　ができる
            msg = arr.remove_space_and_change_commma(str(message.content))
            msg = arr.change_hyphen(msg)
            msg = arr.to_full_half2(msg)
            print(msg)
        except Exception as e:
            print(f"メッセージの標準化に失敗しました。\n{e}")

        try:
            # 各チャンネルの接続設定を行う
            if "$setfirstdaychannel" in msg:
                command, day = msg.split(":")
                channel_id = message.channel.id
                # チャンネルIDをリストに追加
                if channel_id not in channel_list:
                    channel_list[channel_id] = f'シフトうめうめ{day}日目'
                    await message.channel.send(f'A channel with ID {channel_id} was added to the list with the name {channel_list[channel_id]}.')
                else:
                    if str(channel_list[channel_id]) != str(day):
                        channel_list[channel_id] = f'シフトうめうめ{day}日目'
                        await message.channel.send(f'Renamed the channel with ID {channel_id} to {channel_list[channel_id]} in the list.')
                    else:
                        await message.channel.send(f'Channel with ID {channel_id} is already in the list.')

        except Exception as e:
            await message.channel.send("なにかエラーが発生しました。")
            print(f"チャンネル設定エラー\n{e}")

        try:
            # チャンネルIDがchannel_listのキーに含まれているかを確認
                if message.channel.id in channel_list and not "$" in msg and message.reference is None:
                    # 対応するチャンネル名を取得
                    channel_id = message.channel.id
                    channel_name = channel_list[channel_id]
                    try:
                        helper_data = AS.get_helper_info(str(message.author.display_name))
                    except Exception as e:
                        print(f"get_helper_info エラー\n{e}")
                    try:
                        AS.save_helper_shift(str(message.author.display_name), helper_data, channel_name, str(msg))
                        custom_emoji = discord.utils.get(message.guild.emojis, name=custom_emoji_name)
                        await message.add_reaction(custom_emoji)
                    except Exception as e:
                        print(f"save_helper_shift エラー\n{e}")    



        except Exception as e:
            await message.channel.send("なにかエラーが発生しました。")
            print(f"シフトの日取得エラー\n{e}")

    if not message.author.bot:
        try:
            # メッセージを標準形式に変換
            msg = arr.remove_space_and_change_commma(str(message.content))
            if "$setserver" in msg:
                SERVER_ID = message.guild.id
                channel_list = {}
                await message.channel.send(f"使用サーバを{message.guild}に設定しました．")
                print(f"サーバ設定を【{message.guild}({SERVER_ID})】に設定しました．")
        except Exception as e:
            print(f"サーバ設定に失敗しました\n{e}")


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)