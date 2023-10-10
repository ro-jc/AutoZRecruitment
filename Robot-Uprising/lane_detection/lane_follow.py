import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
 
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
 
 
VIDEO_DIMENSIONS = (640, 480)
 
 
def process_frame(image):
    image = cv.GaussianBlur(image, (3,3), 100)
 
 
 
    (_, _, R) = cv.split(image)
    threshold_red = cv.inRange(R, 250, 255)
 
    merged = cv.merge([threshold_red,threshold_red,threshold_red])
 
    roi = np.float32(
           ((200, 92),
            (50, 260),
            (610, 260),
            (440, 92))
        )
 
    pad = 50
    desired = np.float32(
           ((pad, 0),
            (pad, 480),
            (640-pad, 480),
            (640-pad, 0))
        )
 
    transformation_matrix = cv.getPerspectiveTransform(roi, desired)
    # inverse_transformation_matrix = cv.getPerspectiveTransform(desired, roi)
 
    warped_image = cv.warpPerspective(merged, transformation_matrix, VIDEO_DIMENSIONS, flags=(cv.INTER_LINEAR))
 
    cv.imshow('transformed image',warped_image)
    cv.waitKey(1)
 
    # warped_height = warped_image.shape[0]
    # histogram = np.sum(warped_image[warped_height//2:,:], axis=0)
    # mid = np.int(histogram.shape[0]/2)
    # l_max = np.argmax(histogram[:mid])
    # r_max = np.argmax(histogram[mid:]) + mid
    # center = np.int((r_max + l_max)/2)
 
    return warped_image
 
 
def find_center(image, plot=False):
    h = image.shape[0]
    histogram = np.sum(image[:h//2, :], axis=0)
 
    mid = np.int(histogram.shape[0]/2)	#320	
    l_max = np.argmax(histogram[:mid], axis=0)[0]
    r_max = np.argmax(histogram[mid:], axis=0)[0] + mid
 
    center = np.int((l_max+r_max)/2)
    print(f"l:{l_max}-{histogram[l_max]}\tr:{r_max}-{histogram[r_max]}\tlane center:{center}")
 
    if plot:
        figure, (ax1, ax2) = plt.subplots(2,1) # 2 row, 1 columns
        figure.set_size_inches(10, 5)
        ax1.imshow(image, cmap='gray')
        ax1.set_title("Warped Binary Frame")
        ax2.plot(histogram)
        ax2.set_title("Histogram Peaks")
        plt.show()
 
    return center
 
 
# inp = cv.VideoCapture('test.mp4')
 
# fourcc = cv.VideoWriter_fourcc(*'MJPG')
# out = cv.VideoWriter('output.avi', fourcc, 20.0, VIDEO_DIMENSIONS)
 
# while True:
#     ret, in_frame = inp.read()
 
#     if not ret:
#         print('Frame not received. Exiting..')
#         break
 
#     out.write(process_frame(in_frame))
 
# inp.release()
# out.release()
 
 
# def get_frame():
#     rospy.init_node
#     listner = rospy.Subscriber('/camera/')
#     pass
 
# def skidsteer():
#     rospy.init_node('skidsteer', anonymous=True)
 
#     rospy.Subscriber('/camera/color/image_raw', Image, drive)
 
#     command = Twist()
#     command.linear.x = 1
#     command.angular.z = 0
 
#    frame = get_frame()
 
class LaneFollow():
    def __init__(self) -> None:
        rospy.init_node('lane_follow')
 
        self.pub = rospy.Publisher('/cmd_vel', Twist, latch=True, queue_size=10)
 
        rospy.Subscriber('/camera/color/image_raw', Image, self.drive)
        rospy.spin()
 
    def drive(self, image_raw):
        bridge = CvBridge()
        frame = bridge.imgmsg_to_cv2(image_raw)
 
        processed_frame = process_frame(frame)
 
        true_center = processed_frame.shape[1]//2
        print("true center:", true_center)
        center = find_center(processed_frame)
 
        scale_factor = -0.006
 
        command = Twist()
        command.linear.x = 0.8
        command.angular.z = scale_factor*(center - true_center)
 
        self.pub.publish(command)
        print(f'Publishing {command}')
 
if __name__ == '__main__':
    LaneFollow()
