#!/usr/bin/env python3
import os
import requests
import json
import re
import rospy
from robot_arm.srv import Word
from std_msgs.msg import String

apikey = os.environ.get('DEEPL_API_KEY', '')

# 翻訳するテキストを設定
languages = {'ブルガリア語': 'BG', 'チェコ語': 'CS', 'デンマーク語': 'DA', 'ドイツ語': 'DE', 'ギリシャ語': 'EL', '英語': 'EN', 'イギリス英語': 'EN-GB', 'アメリカ英語': 'EN-US', 'スペイン語': 'ES', 'エストニア語': 'ET', 'フィンランド語': 'FI', 'フランス語': 'FR', 'ハンガリー語': 'HU', 'インドネシア語': 'ID', 'イタリア語': 'IT', '韓国語': 'KO', 'リトアニア語': 'LT', 'ラトビア語': 'LV', 'ブークモール語': 'NB', 'オランダ語': 'NL', 'ポーランド語': 'PL', 'ポルトガル語': 'PT', 'ブラジル語': 'PT-BR', 'ルーマニア語': 'RO', 'ロシア語': 'RU', 'スロバキア語': 'SK', 'スロベニア語': 'SL', 'スウェーデン語': 'SV', 'トルコ語': 'TR', 'ウクライナ語': 'UK', '中国語': 'ZH'}
wono=["を","の"]
#"日本語":"JA"は抜いてある
def callback(msg):
    text = msg.data
    for language in languages:
        if language in text:
            ultlanguage=languages[language]
            a=True
            break
    if language in text:
        index = text.index(language)
        text = text[:index - 1]
        print(text)
    # APIエンドポイントのURL
    url = 'https://api-free.deepl.com/v2/translate'
    # POSTリクエストで送信するデータを設定
    data = {
        'auth_key': apikey,
        'text': text,
        'target_lang': ultlanguage,
        'source_lang': 'JA'
    }

    # APIにリクエストを送信して翻訳結果を取得
    response = requests.post(url, data=data)
    result = json.loads(response.content)

    # 翻訳結果を表示
    talk(text + "を" + language + "で言うと、")
    print(text + "を" + language + "で言うと、")
    talk(ultlanguage.lower() + "@" + result['translations'][0]['text'])
    print(ultlanguage.lower() + "@" + result['translations'][0]['text'])

    '''
    def hon1():
        #全部わかる
        pass
    def hon2():
        #国のみ分かる
        pass
    def hon3():
        #を、の
        pass
    def hon4():
        #全部分からん
        pass
    command="a"
    for language in languages:
        if language in text:
            for i in range(2):
                if wono[i] in text:
                    hon1()
                    unnamed1=True
            if unnamed1==False:
                hon2()
                unnamed1=True
    if unnamed1==False:
        for i in range(2):
            if wono[i] in text:
                hon3()
                unnamed1=True
    if unnamed1==False:
        hon4()
    if command=="_____を_____語にして":
        pass
    if command=="_____語にして":
        pass
    if command=="翻訳して":
        pass

    #ジャンル分けを作る(翻訳して、何語にして、原文)を、のを枕詞にして作るといいかも

    text = "私はりんごを食べた。のという言葉の前の文を抜き出したい。"

    # 正規表現パターンを定義
    pattern = r"(?<=。)[^。]+を、のという言葉の前の文"

    # パターンに一致する箇所を検索
    result = re.search(pattern, text)

    # 結果を表示
    if result:
        print(result.group())
    else:
        print("マッチする箇所はありませんでした。")
    '''

if __name__ == '__main__':
    rospy.init_node('translation', anonymous=True)
    talk = rospy.ServiceProxy('/text_talk/srv', Word)
    rospy.Subscriber('/task/translation', String, callback)
    # ノードをループさせる
    rospy.spin()