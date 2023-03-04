import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


VIDEO_DIMENSIONS = (640, 480)

def process_frame(image):
    # image = cv.GaussianBlur(image, (3,3), 100)
    
    white = cv.inRange(image, (100,100,100), (255,255,255))
    cv.imshow('white',white);cv.waitKey(0);cv.destroyAllWindows()
    
    # (_, _, R) = cv.split(image)
    # red = cv.inRange(R, 100, 255)
    lower_red = np.array([0, 0, 10], dtype = "uint8")
    upper_red= np.array([0, 0, 255], dtype = "uint8")
    red_mask = cv.inRange(image, lower_red, upper_red)
    red = cv.bitwise_and(image, image, mask=red_mask)
    cv.imshow('red',red);cv.waitKey(0);cv.destroyAllWindows()

    (B, G, R) = cv.split(image)
    threshold_red = cv.inRange(R, 100, 255)
    threshold_blue = cv.inRange(B, 100, 255)
    threshold_green = cv.inRange(G, 100, 255)
    # cv.imshow('',threshold_red);cv.waitKey(0);cv.destroyAllWindows()
    
    final_mask = (threshold_blue & threshold_green & threshold_red) | threshold_red
    
    
    h = image.shape[0]
    histogram = np.sum(image, axis=0)
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

    warped_image = cv.warpPerspective(final_mask, transformation_matrix, VIDEO_DIMENSIONS, flags=(cv.INTER_LINEAR))

    return warped_image


image = cv.imread('/media/Common/Code/AutoZRecruitment/Robot-Uprising/lane_detection/start.png')
cv.imshow('',image);cv.waitKey(0);cv.destroyAllWindows()
cv.imshow('',process_frame(image));cv.waitKey(0);cv.destroyAllWindows()