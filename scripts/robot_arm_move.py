#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from Adafruit_PCA9685 import PCA9685
import math

servo_min = 100
servo_max = 510

pwm = PCA9685()
pwm.set_pwm_freq(50)

def joint_states_callback(msg):
    joint_angles = msg.position
    print(msg)
    pulse0 = int((servo_max - servo_min)*(math.degrees(joint_angles[1]) + 90) / 180 + servo_min)
    pulse1 = int((servo_max - servo_min)*(180 - math.degrees(joint_angles[1]) - 90) / 180 + servo_min)
    pulse2 = int((servo_max - servo_min)*(math.degrees(joint_angles[2]) + 100) / 180 + servo_min)
    pulse3 = int((servo_max - servo_min)*(180 - math.degrees(joint_angles[2]) - 80) / 180 + servo_min)
    pulse4 = int((servo_max - servo_min)*(math.degrees(joint_angles[3]) + 90) / 180 + servo_min)
    pulse5 = int((servo_max - servo_min)*(math.degrees(joint_angles[4]) + 90) / 180 + servo_min)
    pulse6 = int((servo_max - servo_min)*(math.degrees(joint_angles[5]) + 90) / 180 + servo_min)
    pwm.set_pwm(0, 0, pulse0)
    pwm.set_pwm(1, 0, pulse1)
    pwm.set_pwm(2, 0, pulse2)
    pwm.set_pwm(3, 0, pulse3)
    pwm.set_pwm(4, 0, pulse4)
    pwm.set_pwm(5, 0, pulse5)
    pwm.set_pwm(7, 0, pulse6)

def listener():
    rospy.init_node('robot_arm_move', anonymous=True)
    rospy.Subscriber("/joint_states", JointState, joint_states_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
