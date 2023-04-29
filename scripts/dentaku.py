#!/usr/bin/env python3
import rospy
from robot_arm.srv import Word
from std_msgs.msg import String
import re

def callback(msg):
    suusiki1=msg.data
    if '=' in suusiki1:
        suusiki1 = suusiki1.replace('=','')
    plus=[]
    division=[]
    suuji3=[]
    suuji2=[]
    suuji1=re.split('[+-]',suusiki1)
    for _ in suusiki1:
        if _=='-' or _=='+':
            plus.append(_)
        if _=='×' or _=='÷':
            division.append(_)
    for _ in suuji1:
        a=re.split('[×÷]',_)
        suuji2.append(a)
    for _ in suuji2:
        n1=int(_.pop(0))
        while len(_)!=0:
            n2=int(_.pop(0))
            if division.pop(0)=='×':
                n1=n1*n2
            else:
                n1=n1/n2
        suuji3.append(n1)
    n1=suuji3.pop(0)
    while len(suuji3)!=0:
        n2=suuji3.pop(0)
        if plus.pop(0)=='+':
            n1=n1+n2
        else:
            n1=n1-n2
    talk(suusiki1 + "は" + str(round(n1,3)) + "です")

if __name__ == '__main__':
    rospy.init_node('dentaku', anonymous=True)
    talk = rospy.ServiceProxy('/text_talk/srv', Word)
    rospy.Subscriber('/task/dentaku', String, callback)
    # ノードをループさせる
    rospy.spin()