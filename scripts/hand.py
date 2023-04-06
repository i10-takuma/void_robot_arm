#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from Adafruit_PCA9685 import PCA9685
import time
import math

# サーボモーターの設定
servo_min = 200  # 最小パルス幅 (ms)
servo_max = 430  # 最大パルス幅 (ms)

# PCA9685のI2Cアドレス
pwm = PCA9685(address=0x40)
# PWM周波数
pwm.set_pwm_freq(50)

# 目標角度の受け取り用コールバック関数
def hand_callback(msg):
    print(msg)
    #pulse0 = int((servo_max - servo_min)*(math.degrees(joint_angles[1]) + 90) / 180 + servo_min)

    if msg.data == "open":
        pwm.set_pwm(7, 0, servo_max)
        pwm.set_pwm(6, 0, servo_min)
    
    if msg.data == "close":
        pwm.set_pwm(7, 0, servo_min)
        pwm.set_pwm(6, 0, servo_max)



def listener():
    rospy.init_node('hand_controal', anonymous=True)
    rospy.Subscriber("/hand_move", String, hand_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()