#!/usr/bin/env python3
import rospy
from robot_arm.srv import Word
from std_msgs.msg import String
import aiml
import MeCab


kernel = aiml.Kernel()
kernel.learn("/home/takuma/catkin_ws/src/robot_arm/scripts/aiml.xml")

def callback(msg):
    talk = rospy.ServiceProxy('/text_talk/srv', Word)
    text1 = ""
    task_ID = None
    response = ""
    input_text = msg.data
    if input_text == '止めて':
        task_ID = '/task/stop'
        text1 = 'stop'
    else:
        wakati = MeCab.Tagger('-Owakati')
        wakati_text = wakati.parse(input_text)
        print(wakati_text)
        response = kernel.respond(wakati_text)
        if response == "現在時刻をお伝えします。":
            text1 = input_text
        elif response == "アラームを設定します。":
            text1 = input_text
        elif response == "タイマーを設定します。":
            text1 = input_text
        elif response == "開きます":
            text1 = "open"
            task_ID = '/hand_move'
        elif response == "閉じます":
            text1 = "close"
            task_ID = '/hand_move'
        else:
            if response == "":
                response = "よくわかりませんでした。ごめんなさい"
            print('Bot: ', response)
            talk(response)
    print(task_ID)
    print(text1)
    if task_ID:
        taskpub = rospy.Publisher(str(task_ID), String, queue_size=10)
        taskpub.publish(text1)

if __name__ == '__main__':
    rospy.init_node('dialogue_system', anonymous=True)
    rospy.Subscriber('/greco/msgs', String, callback)
    rospy.spin()
