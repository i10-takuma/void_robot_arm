#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import cv2
import numpy as np
import tf2_ros
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud
from sensor_msgs.msg import Image, CameraInfo, RegionOfInterest, PointCloud2, PointField
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs import point_cloud2
from std_msgs.msg import Header
from darknet_ros_msgs.msg import BoundingBoxes
from sensor_msgs.msg import RegionOfInterest
from robot_arm.srv import Point_trim
from robot_arm.srv import Point_trimResponse


class PointCloudGenerator():
    def __init__(self):
        
        rospy.init_node('point_cloud_generator', anonymous=True)
        
        # パブリッシャーの作成
        self.point_cloud_pub = rospy.Publisher('/point_cloud', PointCloud2, queue_size=1)

        # サブスクライバーの作成
        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.image_callback)
        self.name_srv = rospy.Service("/pick/get_point", Point_trim, self.name_callback)
        self.depth_sub = rospy.Subscriber('/camera/depth_registered/image_raw', Image, self.depth_callback)
        self.info_sub = rospy.Subscriber('/camera/depth_registered/camera_info', CameraInfo, self.info_callback)

        # メンバ変数の初期化
        self.bridge = CvBridge()
        self.camera_info = None
        self.color_image = None
        self.depth_image = None
        self.bounding_boxes = None
        self.target_name = None
        
        rospy.spin()

    def name_callback(self, req):
        # nameを受信し、メンバ変数に保存
        self.target_name = req.name
        while self.bounding_boxes == None:
            boxs = rospy.wait_for_message('/darknet_ros/bounding_boxes', BoundingBoxes, timeout=5.0).bounding_boxes
            for bbox in boxs:
                if bbox.Class == self.target_name:
                    self.bounding_boxes = bbox
        
        points = self.run()
        return Point_trimResponse(point = points)

    def image_callback(self, data):
        # RGB画像を受信し、メンバ変数に保存
        try:
            self.color_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

    def depth_callback(self, data):
        # Depth画像を受信し、メンバ変数に保存
        try:
            self.depth_image = self.bridge.imgmsg_to_cv2(data, "16UC1")
        except CvBridgeError as e:
            print(e)

    def info_callback(self, data):
        # infoを受信し、メンバ変数に保存
        self.camera_info = data

    def run(self):
        if self.color_image is not None and self.depth_image is not None and self.bounding_boxes is not None and self.camera_info is not None:
            # バウンディングボックスの範囲にあるRGBD画像をトリミング
            roi = RegionOfInterest(x_offset=self.bounding_boxes.xmin - 10  , y_offset=self.bounding_boxes.ymin - 10, width=self.bounding_boxes.xmax  - self.bounding_boxes.xmin + 20 , height=self.bounding_boxes.ymax - self.bounding_boxes.ymin + 20 )
            color_image_roi = self.color_image[roi.y_offset:roi.y_offset+roi.height, roi.x_offset:roi.x_offset+roi.width]
            depth_image_roi = self.depth_image[roi.y_offset:roi.y_offset+roi.height, roi.x_offset:roi.x_offset+roi.width]

            # RGB画像をBGRからRGBに変換
            try:
                color_image_roi = cv2.cvtColor(color_image_roi, cv2.COLOR_BGR2RGB)
            except cv2.error as e:
                print("error")

            # Depth画像をfloat型に変換
            depth_image_roi = depth_image_roi.astype(np.float32)

            # Depth画像をメートルに変換
            depth_image_roi = depth_image_roi / 1000.0
            
            tf_buffer = tf2_ros.Buffer()
            tf_listener = tf2_ros.TransformListener(tf_buffer)

            
            # PointCloud2を生成してパブリッシュ
            header = Header()
            header.stamp = rospy.Time.now()
            header.frame_id = 'camera_rgb_optical_frame'

            points = []
            for v in range(roi.y_offset, roi.y_offset+roi.height):
                for u in range(roi.x_offset, roi.x_offset+roi.width):
                    z = depth_image_roi[v-roi.y_offset, u-roi.x_offset] 
                    if z == 0:
                        continue
                    x = (u - self.camera_info.K[2]) * z / self.camera_info.K[0] 
                    y = (v - self.camera_info.K[5]) * z / self.camera_info.K[4] 
                    r,g,b = color_image_roi[v-roi.y_offset, u-roi.x_offset]
                    rgb = np.array((r << 16) | (g << 8 ) | (b << 0),dtype=np.uint32)
                    color = rgb.reshape(-1,1)
                    rgb.dtype = np.float32
                    points.append([x, y, z, rgb])

            #print(points)
            #print(color)
            points = np.array(points, dtype=np.float32)
            fields = [PointField('x', 0, PointField.FLOAT32, 1),
                      PointField('y', 4, PointField.FLOAT32, 1),
                      PointField('z', 8, PointField.FLOAT32, 1),
                      PointField("rgb",12,PointField.FLOAT32,1)]
            points_np = np.array(points, dtype=np.float32)
            cloud = point_cloud2.create_cloud(header, fields, points_np)
            
            try:
                transform = tf_buffer.lookup_transform('base_link', cloud.header.frame_id, rospy.Time(), rospy.Duration(1.0))
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                rospy.logwarn("Transform lookup failed: {}".format(e))
                return
            
            # PointCloud2を変換
            transformed_cloud = do_transform_cloud(cloud, transform)
            
            # 変換後のPointCloud2をパブリッシュ
            self.point_cloud_pub.publish(transformed_cloud)
            print("yes")

            # メンバ変数の初期化
            self.color_image = None
            self.depth_image = None
            self.bounding_boxes = None
            
            return transformed_cloud

if __name__ == '__main__':
    try:
        pcg = PointCloudGenerator()
        pcg.__init__()
    except rospy.ROSInterruptException:
        pass
