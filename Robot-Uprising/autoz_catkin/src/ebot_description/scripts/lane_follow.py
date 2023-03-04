#!/usr/bin/env python

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist


VIDEO_DIMENSIONS = (640, 480)

    
class LaneFollow():
    def __init__(self) -> None:
        rospy.init_node('lane_follow', anonymous=True)
        
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        rospy.Subscriber('/camera/color/image_raw', Image, self.drive)
        rospy.spin()

 
    def process_frame(self):
        # image = cv.GaussianBlur(image, (3,3), 100)

        (B, G, R) = cv.split(self.raw_frame)
        threshold_red = cv.inRange(R, 100, 255)
        threshold_blue = cv.inRange(B, 100, 255)
        threshold_green = cv.inRange(G, 100, 255)
        # cv.imshow('',threshold_red);cv.waitKey(0);cv.destroyAllWindows()
        
        final_mask = (threshold_red & threshold_blue & threshold_green) | threshold_red

        # merged = cv.merge([final_mask,final_mask,final_mask])

        roi = np.float32(
            ((200, 92),
                (50, 260),
                (610, 260),
                (440, 92))
            )

        pad = 80
        desired = np.float32(
            ((pad, 0),
                (pad, 480),
                (640-pad, 480),
                (640-pad, 0))
            )

        transformation_matrix = cv.getPerspectiveTransform(roi, desired)
        # inverse_transformation_matrix = cv.getPerspectiveTransform(desired, roi)

        warped_image = cv.warpPerspective(final_mask, transformation_matrix, VIDEO_DIMENSIONS, flags=(cv.INTER_LINEAR))

        self.processed_frame = warped_image
        # image = cv.GaussianBlur(self.raw_frame, (3,3), 100)

        # (B, G, R) = cv.split(image)
        # threshold_red = cv.inRange(R, 100, 255)
        # threshold_blue = cv.inRange(B, 100, 255)
        # threshold_green = cv.inRange(G, 100, 255)
        # # cv.imshow('',threshold_red);cv.waitKey(0);cv.destroyAllWindows()
        
        # final_mask = (threshold_red & threshold_blue & threshold_green) | threshold_red
        # cv.imshow('final_mask',threshold_red);cv.waitKey(0);cv.destroyAllWindows()

        # merged = cv.merge([final_mask,final_mask,final_mask])

        # roi = np.float32(
        #     ((200, 92),
        #         (50, 260),
        #         (610, 260),
        #         (440, 92))
        #     )

        # pad = 80
        # desired = np.float32(
        #     ((pad, 0),
        #         (pad, 480),
        #         (640-pad, 480),
        #         (640-pad, 0))
        #     )

        # transformation_matrix = cv.getPerspectiveTransform(roi, desired)
        # # inverse_transformation_matrix = cv.getPerspectiveTransform(desired, roi)

        # self.processed_frame = cv.warpPerspective(merged, transformation_matrix, VIDEO_DIMENSIONS, flags=(cv.INTER_LINEAR))


    def find_center(self, plot=False):
        image = self.processed_frame
        h = image.shape[0]
        histogram = np.sum(image[h//2:, :], axis=0)
        cv.imshow('Histogram', image);cv.waitKey(0);cv.destroyAllWindows()
        # histogram = np.sum(image, axis=0)
        
        mid = np.int(histogram.shape[0]/2)
        
        l_max = np.argmax(histogram[:mid-50])
        r_max = np.argmax(histogram[mid+50:]) + mid
        
        self.center = np.int((l_max+r_max)/2)
        
        if plot:
            figure, (ax1, ax2) = plt.subplots(2,1)
            figure.set_size_inches(10, 5)
            ax1.imshow(image, cmap='gray')
            ax1.set_title("Warped Binary Frame")
            ax2.plot(histogram)
            ax2.set_title("Histogram Peaks")
            plt.show()
            sleep(0.1)
            plt.close()


    def drive(self, image_raw):
        bridge = CvBridge()
        self.raw_frame = bridge.imgmsg_to_cv2(image_raw)
        
        self.process_frame()
        cv.imshow('pre-Histogram',self.processed_frame);cv.waitKey(0);cv.destroyAllWindows()
        self.find_center()
        cv.imshow('post-Histogram',self.processed_frame);cv.waitKey(0);cv.destroyAllWindows()
        
        # fourcc = cv.VideoWriter_fourcc(*'MJPG')
        # out = cv.VideoWriter('output.avi', fourcc, 20.0, VIDEO_DIMENSIONS)
        # out.write(processed_frame)
        
        true_center = 320
        print(f'true center: {true_center}\tcenter: {self.center}')
        
        scale_factor = -0.01
        angular = scale_factor * (self.center - true_center)

        if abs(angular) < 0.5:
            angular = 0
        
        command = Twist()
        command.linear.x = 0.75
        command.angular.z = angular
        
        self.pub.publish(command)
        print(f'Publishing {command}')


if __name__ == '__main__':
    try:
        LaneFollow()
    except rospy.ROSInterruptException:
        print('Exiting..')