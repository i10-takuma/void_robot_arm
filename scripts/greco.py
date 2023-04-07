#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import speech_recognition as sr

def speech_recognition_callback(data):
    if data.data == 'hotword_detection':
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("音声認識を開始します")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ja-JP")
            print("音声認識の結果: " + text)
            if text != "":
                pub.publish(text)
        except sr.UnknownValueError:
            print("聞き取れませんでした")
        except sr.RequestError as e:
            print("リクエストの処理中にエラーが発生しました: {}".format(e))

def listener():
    rospy.init_node('speech_recognition_node', anonymous=True)
    rospy.Subscriber('/hotword_detection', String, speech_recognition_callback)
    rospy.spin()

if __name__ == '__main__':
    pub = rospy.Publisher('/greco/msgs', String, queue_size=10)
    listener()
