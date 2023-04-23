#!/usr/bin/env python3
import rospy
from robot_arm.srv import Word
from std_msgs.msg import String
import aiml
import MeCab
import moveit_commander
import sys


kernel = aiml.Kernel()
kernel.learn("/home/takuma/catkin_ws/src/robot_arm/scripts/aiml.xml")

def callback(msg): 
    talk = rospy.ServiceProxy('/text_talk/srv', Word)
    text1 = ""
    task_ID = None
    response = ""
    object = ''
    word = ''
    input_text = msg.data
    #input_text = input_text.replace(' ', '')
    if input_text == '止めて':
        task_ID = '/task/stop'
        text1 = 'stop'
    else:
        wakati = MeCab.Tagger('-Owakati')
        wakati_text = wakati.parse(input_text)
        print(wakati_text)
        response = kernel.respond(wakati_text)
        if response == "天気情報サービスを起動します。":
            text1 = input_text
            task_ID = '/task/weather'
        elif response == "音楽システムを起動します。":
            text1 = input_text  
            task_ID = '/task/spotify' 
        elif response == "現在時刻をお伝えします。":
            text1 = input_text
        elif response == "アラームを設定します。":
            text1 = input_text
        elif response == "タイマーを設定します。":
            text1 = input_text
        elif response == "しりとりをします":
            text1 = "start"
            task_ID = '/task/shiritori'
        elif response == "検索します。":
            word = kernel.getPredicate("search_word")
            text1 = word
            task_ID = '/task/wiki'
        elif response == "開きます":
            text1 = "open"
            task_ID = '/hand_move'
        elif response == "閉じます":
            text1 = "close"
            task_ID = '/hand_move'
        elif response == "動かします":
            text1 = input_text
            task_ID = '/task/manual'
        elif response == "向きます":
            text1 = input_text
            task_ID = '/task/vector'
        elif response == "翻訳します":
            text1 = input_text
            task_ID = '/task/translation'
        elif response == "ダジャレを考えます。":
            text1 = 'dajare'
            task_ID = '/task/joke'
        elif response == "ジョークを考えます。":
            text1 = 'joke'
            task_ID = '/task/joke'
        elif response == "じゃんけんしましょう":
            text1 = 'start'
            task_ID = '/task/janken'
        elif response == "楽天で検索します":
            text1 = kernel.getPredicate("rakuten_search")
            task_ID = '/task/rakuten'
        elif response == "戻ります":
            arm = moveit_commander.MoveGroupCommander("shikigami")
            moveit_commander.roscpp_initialize(sys.argv)
            home = arm.get_named_target_values("home")
            print(home)
            arm.set_joint_value_target(home)
            plan = arm.go(wait=True)
            arm.stop()
            arm.clear_pose_targets()
        elif ("を持ってきます。" in response) or ("をつかみます。" in response) or ("を取ってきます。" in response):
            object = kernel.getPredicate("grab_object")
            text1 = object
            task_ID = '/task/grab_target'
        else:
            if response == "":
                response = "よくわかりませんでした。ごめんなさい"
            print('Bot: ',response)
            talk(response)    
    print(task_ID)
    print(text1)
    taskpub = rospy.Publisher(str(task_ID), String, queue_size=10) 
    taskpub.publish(text1) 

if __name__ == '__main__':
    rospy.init_node('dialogue_system', anonymous=True) #ROS内での名前を定義
    rospy.Subscriber('/greco/msgs', String, callback) #音声認識された文を受信し、callback変数を動かす
    rospy.spin() #ループ