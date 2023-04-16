#!/usr/bin/env python3

import re
import rospy
import requests
from robot_arm.srv import Word
from std_msgs.msg import String
#import wikipedia

# メディアウィキAPIエンドポイント
API_ENDPOINT = "https://ja.wikipedia.org/w/api.php"
#wikipedia.set_lang("jp")

# ページコンテンツを取得する関数
def get_page_content(title):
    # APIに渡すパラメーター
    title = title.replace(' ', '')
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": title,
        "exintro": "",
        "explaintext": "",
        "redirects": "",
        "formatversion": "2"
    }
    # APIリクエストを送信
    response = requests.get(API_ENDPOINT, params=params)
    # レスポンスJSONを取得
    json_data = response.json()
    # ページコンテンツを取得
    try:
        page_content = json_data["query"]["pages"][0]["extract"]
        page_content = ("以下はウィキペディアからの引用です。" + page_content)
    except KeyError:
        page_content = ("申し訳ございません。" + title + "に該当する記事を見つけられませんでした。")
    # 改行コードを削除
    page_content = page_content.replace('\n', '')
    # 括弧と括弧の中身を削除
    page_content = re.sub('（.*?）', '', page_content)
    page_content = re.sub('/(.*?/)', '', page_content)
    return page_content.strip()

# /wiki_titleからタイトルを受信したときに実行されるコールバック関数
def wiki_title_callback(msg):
    # ページコンテンツを取得
    page_content = (get_page_content(msg.data))
    print(page_content)
    # /open_jtalkにパブリッシュ
    talk(str(page_content))

if __name__ == '__main__':
    # ROSノードを初期化
    rospy.init_node('wikipedia', anonymous=True)
    # /wiki_titleからタイトルを受信するためのサブスクライバーを作成
    rospy.Subscriber("/task/wiki", String, wiki_title_callback)
    talk = rospy.ServiceProxy('text_talk/srv', Word)
    # ノードをループさせる
    rospy.spin()
