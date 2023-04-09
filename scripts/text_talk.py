#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from robot_arm.srv import Word
from robot_arm.srv import WordResponse
from gtts import gTTS
import os
import subprocess
from pydub import AudioSegment
from io import BytesIO

# 音声再生用のサブプロセスを保持する変数
play_process = None

def text_to_speech(text):
    global play_process
    hand = rospy.Publisher("/hand_move", String, queue_size=10) 
    mp3_fp = BytesIO()
    # 音声再生中に再度音声変換が要求された場合に備えて、前回の再生を強制停止する
    if play_process is not None:
        play_process.kill()
    
    # @の位置を取得
    index_at = text.find("@")
    if index_at != -1:
        # @の前後の文字列を取得
        lg = text[:index_at]
        print(lg)
        text = text[index_at+1:]
    else:
        lg = 'ja'
    tts = gTTS(text=text, lang=lg)
    temp_mp3_path = "/tmp/temp.mp3"
    hand.publish("open")
    # バイナリデータを扱うためのメモリストリームを作成
    mp3_fp = BytesIO()
    tts.save(temp_mp3_path)

    # Pydubで音声データを読み込み、音量を1.5倍にする
    sound = AudioSegment.from_file(temp_mp3_path, format="mp3")
    sound = sound + 10.0 # 音量を1.5倍にする
    sound.export(temp_mp3_path, format="mp3")
    # 音声を再生
    play_process = subprocess.Popen(['mpg123', '-l', '5', temp_mp3_path])
    play_process.wait()
    hand.publish("bot")
    return "OK"

def callback(msg):
    # メッセージを受信したら、発音する
    text_to_speech(msg.data)

def srv_callback(msg):
    text = text_to_speech(msg.data)
    return WordResponse(text)

def hotword_callback(msg):
    global play_process
    # /hotword_detection トピックから "hotword_detection" メッセージを受信した場合、再生中の音声を強制停止する
    if msg.data == "hotword_detection":
        if play_process is not None:
            play_process.kill()

def listener():
    # ノードを初期化して、メッセージを購読する
    rospy.init_node('text_to_speech')
    rospy.Subscriber('/text_talk', String, callback)
    srv = rospy.Service('/text_talk/srv', Word, srv_callback)
    rospy.Subscriber('/hotword_detection', String, hotword_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
