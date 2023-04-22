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
    tagger = MeCab.Tagger('-Ochasen')
    words = mecab.parse(command).strip().split(" ")
    node = tagger.parseToNode(command)
    numbers = []
    while node:
        # 数字の場合、リストに格納
        if node.feature.split(',')[0] == '名詞' and node.feature.split(',')[1] == '数':
            numbers.append(node.surface)
        node = node.next
    
    current_pose = arm.get_current_pose() #現在の姿勢を取得
    print(node)
    target_pose = current_pose
    for i, word in enumerate(words):
        if word == "右":
            target_pose.pose.position.y += float(numbers[0])/100
        elif word == "左":
            target_pose.pose.position.y -= float(numbers[0])/100
        elif word == "上":
            target_pose.pose.position.z += float(numbers[0])/100
        elif word == "下":
            target_pose.pose.position.z -= float(numbers[0])/100
        elif word == "前":
            target_pose.pose.position.x += float(numbers[0])/100
        elif word == "後ろ":
            target_pose.pose.position.x -= float(numbers[0])/100
    
    arm.set_pose_target(target_pose)
    # 掴み前の位置までの動作をプランし、実行
    print(target_pose)
    plan = arm.go(wait=True)
    arm.stop()
    arm.clear_pose_targets()
    

if __name__ == '__main__':
    rospy.init_node('manual')
    rospy.Subscriber("/task/manual", String, callback)
    talk = rospy.Publisher('/text_talk', String, queue_size=10)
    rospy.spin()
