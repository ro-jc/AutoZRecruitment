import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

import rospy
from geometry_msgs.msg import Twist


VIDEO_DIMENSIONS = (640, 480)


def process_frame(img):
    img = cv.GaussianBlur(img, (3,3), 100)

    (_, _, R) = cv.split(img)
    threshold_red = cv.inRange(R, 100, 255)

    merged = cv.merge([threshold_red,threshold_red,threshold_red])

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
    inverse_transformation_matrix = cv.getPerspectiveTransform(desired, roi)

    warped_image = cv.warpPerspective(merged, transformation_matrix, VIDEO_DIMENSIONS, flags=(cv.INTER_LINEAR))
    warped_height = warped_image.shape[0]
    histogram = np.sum(warped_image[warped_height//2:,:], axis=0)
    mid = np.int(histogram.shape[0]/2)
    l_max = np.argmax(histogram[:mid])
    r_max = np.argmax(histogram[mid:]) + mid
    center = np.int((r_max + l_max)/2)
    # Draw both the image and the histogram
    # figure, (ax1, ax2) = plt.subplots(2,1) # 2 row, 1 columns
    # figure.set_size_inches(10, 5)
    # ax1.imshow(warped_image, cmap='gray')
    # ax1.set_title("Warped Binary Frame")
    # ax2.plot(histogram)
    # ax2.set_title("Histogram Peaks")
    # plt.show()
        
    out = warped_image

    return out


inp = cv.VideoCapture('test.mp4')

fourcc = cv.VideoWriter_fourcc(*'MJPG')
out = cv.VideoWriter('output.avi', fourcc, 20.0, VIDEO_DIMENSIONS)

while True:
    ret, in_frame = inp.read()

    if not ret:
        print('Frame not received. Exiting..')
        break
    
    out.write(process_frame(in_frame))

inp.release()
out.release()


def get_frame():
    listner = rospy.Subscriber('/camera/')
    pass

def skidsteer_node():
    command = Twist()
    command.linear.x = 1
    command.angular.z = 0
    
    frame = get_frame()