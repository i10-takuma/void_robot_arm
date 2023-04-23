#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import sys
import moveit_commander
import numpy
from robot_arm.srv import Point_trim
from robot_arm.srv import Word
from robot_arm.srv import WordResponse
from std_msgs.msg import String
from geometry_msgs.msg import Quaternion, Vector3
from gpd_ros.srv import detect_grasps
from gpd_ros.msg import CloudIndexed
from gpd_ros.msg import CloudSources
from geometry_msgs.msg import Pose
import tf.transformations as tf
import geometry_msgs.msg as geometry_msgs
import numpy as np
import time
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive



class GrabObjectServer():
    def __init__(self):
        # ノードの初期化
        rospy.init_node('grab_object_server', anonymous=True)
        self.ob = {"ボトル":"bottle", "カップ":"cup", "バナナ":"banana"}
        
        # MoveIt関連の初期化
        moveit_commander.roscpp_initialize(sys.argv)
        scene = moveit_commander.PlanningSceneInterface()
        self.arm = moveit_commander.MoveGroupCommander("shikigami")
        #机に衝突判定を与える
        box_pose = geometry_msgs.PoseStamped()
        box_pose.header.frame_id = "base_link"
        box_pose.pose.orientation.w = 1.0
        box_pose.pose.position.x = 0.4
        box_pose.pose.position.z = -0.04 
        box_name = "box"
        scene.add_box(box_name, box_pose, size=(1, 1.5, 0.08))
        
        # サービスの宣言
        self.name = rospy.Subscriber("/task/grab_target", String, self.grab_callback)
        rospy.spin()


    def grab_callback(self, req):
        hand = rospy.Publisher("/hand_move", String, queue_size=10) 
        self.arm.set_planning_time(5)
        hand.publish("open")
        
        rospy.wait_for_service('/pick/get_point')
        name = req.data
        name = self.ob[name]
        
        try:
            get_point = rospy.ServiceProxy('/pick/get_point', Point_trim)
            response = get_point(name)
            point_cloud = response.point
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s", e)
        
        cloud_indexed = CloudIndexed()
        cloud_sources = CloudSources()
        
        cloud_sources.cloud = point_cloud
        indices = [] #Int64(i) for i in range(len(point_cloud.data))
        cloud_indexed.indices = indices
        view_points = []
        camera_source = []
        cloud_sources.view_points = view_points
        cloud_sources.camera_source = camera_source
        cloud_indexed.cloud_sources = cloud_sources
        
        rospy.wait_for_service('/detect_grasps_server/detect_grasps')
        try:
            get_point = rospy.ServiceProxy('/detect_grasps_server/detect_grasps', detect_grasps)
            response = get_point(cloud_indexed)
            grab_poses = response.grasp_configs
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s", e)
        
        i = 0
        grasp = grab_poses.grasps[0]
        '''
        if grasp.axis.z < 0:
            while grasp.axis.z < 0:
                print("now:" + str(i))
                print(grasp)
                if i == 6:
                    break
                grasp = grab_poses.grasps[i + 1]
                i = i + 1
        '''
        # 掴み位置を設定
        grasp_pose = Pose()
        grasp_pose.position.x = grasp.position.x + 0.05 * grasp.approach.x
        grasp_pose.position.y = grasp.position.y + 0.05 * grasp.approach.y
        grasp_pose.position.z = grasp.position.z + 0.05 * grasp.approach.z
        orientation_matrix = [
        [grasp.approach.x, grasp.binormal.x, grasp.axis.x],
        [grasp.approach.y, grasp.binormal.y, grasp.axis.y],
        [grasp.approach.z, grasp.binormal.z, grasp.axis.z],
        ]
        print(orientation_matrix)
        
        orientation_matrix_4x4 = np.zeros((4, 4))
        orientation_matrix_4x4[:3, :3] = orientation_matrix
        orientation_matrix_4x4[3, 3] = 1.0
        orientation_quat = tf.quaternion_from_matrix(orientation_matrix_4x4)
        grasp_pose.orientation = geometry_msgs.Quaternion(*orientation_quat)
        
        # 掴み前の位置を設定
        pre_grasp_pose = Pose()
        pre_grasp_pose.position.x = grasp.position.x - 0.10 * grasp.approach.x
        pre_grasp_pose.position.y = grasp.position.y - 0.10 * grasp.approach.y
        pre_grasp_pose.position.z = grasp.position.z - 0.10 * grasp.approach.z
        pre_grasp_pose.orientation = grasp_pose.orientation
        
        bf_grasp_pose = Pose()
        bf_grasp_pose.position.x = grasp.position.x
        bf_grasp_pose.position.y = grasp.position.y
        bf_grasp_pose.position.z = grasp.position.z + 0.3
        bf_grasp_pose.orientation = grasp_pose.orientation
        
        # アームを掴み前の位置に動かす
        self.moveit(pre_grasp_pose, 0.2)
        
        time.sleep(1)
        
        self.moveit(grasp_pose, 0.1)
        hand.publish("bot")

        time.sleep(1)
        
        home = self.arm.get_named_target_values("home")
        print(home)
        self.arm.set_joint_value_target(home)
        plan = self.arm.go(wait=True)
        self.arm.stop()
        self.arm.clear_pose_targets()

    def moveit(self, pose, t):
        self.arm
        self.arm.set_goal_orientation_tolerance(t)
        self.arm.set_pose_target(pose)
        plan = self.arm.go(wait = True)
        self.arm.stop()
        self.arm.clear_pose_targets()

if __name__ == '__main__':
    try:
        pcg = GrabObjectServer()
        pcg.__init__()
    except rospy.ROSInterruptException:
        pass
