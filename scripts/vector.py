#!/usr/bin/env python3
import rospy
import MeCab
import sys
import moveit_commander
from geometry_msgs.msg import Pose
from std_msgs.msg import String
import geometry_msgs.msg as geometry_msgs
from geometry_msgs.msg import PoseStamped
from robot_arm.srv import Word
from moveit_msgs.msg import MoveGroupAction, MoveGroupGoal, MoveItErrorCodes

def callback(data):
    arm = moveit_commander.MoveGroupCommander("shikigami")
    moveit_commander.roscpp_initialize(sys.argv)
    #Mecabで命令文を解析
    command = data.data
    mecab = MeCab.Tagger("-Owakati")
    words = mecab.parse(command).strip().split(" ")
    
    current_pose = arm.get_current_pose() #現在の姿勢を取得
    print(current_pose)
    target_pose = current_pose
    for i, word in enumerate(words):
        if word == "右":
            print("対応していません")
        elif word == "左":
            print("対応していません")
        elif word == "上":
            print("対応していません")
        elif word == "下":
            target_pose.pose.orientation.x = 0
            target_pose.pose.orientation.y = 0.7149906219580777
            target_pose.pose.orientation.z = 0
            target_pose.pose.orientation.w = 0.6991340369093493
        elif word == "前":
            target_pose.pose.orientation.x = 0
            target_pose.pose.orientation.y = 0
            target_pose.pose.orientation.z = 0
            target_pose.pose.orientation.w = 1
        elif word == "後ろ":
            print("対応していません")
    
    arm.set_pose_target(target_pose)
    # 掴み前の位置までの動作をプランし、実行
    print(target_pose)
    plan = arm.go(wait=True)
    arm.stop()
    arm.clear_pose_targets()

if __name__ == '__main__':
    rospy.init_node('vector', anonymous=True)
    rospy.Subscriber("/task/vector", String, callback)
    talk = rospy.Publisher('/text_talk', String, queue_size=10)
    rospy.spin()
