#!/usr/bin/env python3
import os
import rospy
from robot_arm.srv import Word
from std_msgs.msg import String
import requests
import json

def callback(msg):
    item_name = msg.data

    appid = os.environ.get('YAHOO_API_KEY', '')
    url = 'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?appid={}&query={}&results=1'.format(appid,  item_name)
    call = requests.get(url)
    res_dict = json.loads(call.content)
    count = len(res_dict['hits'])

    for i in range(count):
        talk(res_dict['hits'][i]['name'] + "という商品が見つかりました")
        print(res_dict['hits'][i]['name'])
        talk("価格は" + str(res_dict['hits'][i]['price']) + "円です")
        print("商品URL", res_dict['hits'][i]['url'])
    talk("本来購入することも出来ますが、購入されるとヤバイので抵抗します、拳で")

if __name__ == '__main__':
    rospy.init_node('rakuten', anonymous=True)
    talk = rospy.ServiceProxy('/text_talk/srv', Word)
    rospy.Subscriber('/task/rakuten', String, callback)
    # ノードをループさせる
    rospy.spin()