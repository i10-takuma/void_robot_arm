#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import wiringpi
import time
import math

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(12, 1)

# 目標角度の受け取り用コールバック関数
def hand_callback(msg):
    print(msg)
    
    if msg.data == "on":
        wiringpi.digitalWrite(12, 1)
    
    if msg.data == "off":
        wiringpi.digitalWrite(12, 0)


def listener():
    rospy.init_node('led_controal', anonymous=True)
    rospy.Subscriber("/led_on", String, hand_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()