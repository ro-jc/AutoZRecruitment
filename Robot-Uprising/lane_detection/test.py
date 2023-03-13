import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


VIDEO_DIMENSIONS = (640, 480)

def process_frame(image):
    # image = cv.GaussianBlur(image, (3,3), 100)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    
    hsv_low = np.array([168, 228, 100], np.uint8)
    hsv_high = np.array([179, 255, 255], np.uint8)
    mask = cv.inRange(hsv, hsv_low, hsv_high)
    cv.imshow('mask',mask);cv.waitKey(0);cv.destroyAllWindows()
    
    res = cv.bitwise_and(hsv, hsv, mask=mask)
    
    cv.imshow('res',res);cv.waitKey(0);cv.destroyAllWindows()
    
    
    h = res.shape[0]
    histogram = np.sum(mask, axis=0)
    # print(np.argmax(histogram))
    print(histogram.shape)
    mid = np.int(histogram.shape[0]/2)
    print('mid',mid)
    l_max = np.argmax(histogram[:mid])
    r_max = np.argmax(histogram[mid:]) + mid
    print(l_max,r_max)
    center = np.int((l_max+r_max)/2)
    print(center)
    # merged = cv.merge([final_mask,final_mask,final_mask])
    # print(merged.shape)

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

    warped_image = cv.warpPerspective(res, transformation_matrix, VIDEO_DIMENSIONS, flags=(cv.INTER_LINEAR))

    return warped_image


image = cv.imread('/media/Common/Code/AutoZRecruitment/Robot-Uprising/lane_detection/start.png')
cv.imshow('',image);cv.waitKey(0);cv.destroyAllWindows()
cv.imshow('',process_frame(image));cv.waitKey(0);cv.destroyAllWindows()