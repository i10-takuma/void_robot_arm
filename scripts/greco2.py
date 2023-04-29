#!/usr/bin/env python3
import rospy
import time
from std_msgs.msg import String
from robot_arm.srv import Word
from robot_arm.srv import WordResponse
import speech_recognition as sr
from speech_recognition import Microphone, Recognizer

def recognize_with_timeout(recognizer, audio, timeout):
    start_time = time.time()
    transcribed = []
    while time.time() - start_time < timeout:
        try:
            text = recognizer.recognize_google(audio, language="ja-JP")
            led.publish("off")
            return text
            break
        except sr.UnknownValueError:
            print("聞き取れませんでした")
        except sr.RequestError as e:
            transcribed.append("リクエストの処理中にエラーが発生しました: {}".format(e))
    return ""

def speech_recognition_callback(data):
    if data.data == 'hotword_detection':
        led.publish("on")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("音声認識を開始します")
            audio = r.listen(source)
        text = recognize_with_timeout(r, audio, 1)
        print("音声認識の結果: " + text)
        led.publish("off")
        if text != "":
            pub.publish(text)

def handle_service(req):
    led.publish("on")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("音声認識を開始します")
        audio = r.listen(source)
    text = recognize_with_timeout(r, audio, 1)
    led.publish("off")
    return WordResponse(text)

def listener():
    rospy.init_node('speech_recognition_node', anonymous=True)
    rospy.Subscriber('/hotword_detection', String, speech_recognition_callback)
    s = rospy.Service('/greco/reply', Word, handle_service)
    rospy.spin()

if __name__ == '__main__':
    pub = rospy.Publisher('/greco/msgs', String, queue_size=10)
    led = rospy.Publisher('/led_on', String, queue_size=10)
    listener()
