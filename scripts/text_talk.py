#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from robot_arm.srv import Word
from robot_arm.srv import WordResponse
from gtts import gTTS
import subprocess
from pydub import AudioSegment
from io import BytesIO

play_process = None

def text_to_speech(text):
    global play_process
    if play_process is not None:
        play_process.kill()
    tts = gTTS(text=text, lang='ja')
    temp_mp3_path = "/tmp/temp.mp3"
    tts.save(temp_mp3_path)
    sound = AudioSegment.from_file(temp_mp3_path, format="mp3")
    sound = sound + 10.0
    sound.export(temp_mp3_path, format="mp3")
    play_process = subprocess.Popen(['mpg123', '-l', '5', temp_mp3_path])
    play_process.wait()
    return "OK"

def callback(msg):
    text_to_speech(msg.data)

def srv_callback(msg):
    text = text_to_speech(msg.data)
    return WordResponse(text)

def listener():
    rospy.init_node('text_to_speech')
    rospy.Subscriber('/text_talk', String, callback)
    srv = rospy.Service('/text_talk/srv', Word, srv_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
