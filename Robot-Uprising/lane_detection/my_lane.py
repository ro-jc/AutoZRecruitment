import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


VIDEO_DIMENSIONS = (640, 480)


def process_frame(img):
    img = cv.GaussianBlur(img, (3,3), 100)
    # cv.imshow('gaussian blur', img);cv.waitKey(0);cv.destroyAllWindows()

    (_, _, R) = cv.split(img)
    threshold_red = cv.inRange(R, 100, 255)

    merged = cv.merge([threshold_red,threshold_red,threshold_red])
    # cv.imshow('result red', white_and_red);cv.waitKey(0);cv.destroyAllWindows()

    roi = np.float32(
           ((200, 92),
            (50, 260),
            (610, 260),
            (440, 92))
        )

    pad = 160
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
    # Draw both the image and the histogram
    # figure, (ax1, ax2) = plt.subplots(2,1) # 2 row, 1 columns
    # figure.set_size_inches(10, 5)
    # ax1.imshow(warped_image, cmap='gray')
    # ax1.set_title("Warped Binary Frame")
    # ax2.plot(histogram)
    # ax2.set_title("Histogram Peaks")
    # plt.show()
    
    margin = 54
    sliding_window = warped_image.copy()
    windows_num = 20
    window_height = np.int(warped_height/windows_num)
    nonz = warped_image.nonzero()
    nonz_y, nonz_x = nonz[0], nonz[1]
    
    l_inds = []
    r_inds = []
    
    l_current = l_max
    r_current = r_max
    
    for window in range(windows_num):
        y_low = warped_height - (window + 1) * window_height
        y_high = warped_height - window * window_height
        l_low = l_current - margin
        l_high = l_current + margin
        r_low = l_current - margin
        r_high = l_current + margin
        
        good_l_inds = ((nonz_y >= y_low) & (nonz_y < y_high) & (nonz_x >= l_low) & (nonz_x < l_high)).nonzero()[0]
        good_r_inds = ((nonz_y >= y_low) & (nonz_y < y_high) & (nonz_x >= r_low) & (nonz_x < r_high)).nonzero()[0]
        l_inds.append(good_l_inds)
        r_inds.append(good_r_inds)
        
        minpix = 27
        if len(good_l_inds) > minpix:
            l_current = np.int(np.mean(nonz_x[good_l_inds]))
        if len(good_r_inds) > minpix:
            r_current = np.int(np.mean(nonz_x[good_r_inds]))
            
    l_inds = np.concatenate(l_inds)
    r_inds = np.concatenate(r_inds)
    
    l_x = nonz_x[l_inds]
    l_y = nonz_y[l_inds]
    r_x = nonz_x[r_inds]
    r_y = nonz_y[r_inds]
    
    # # print(l_x!=[], l_y, r_x, r_y)
    
    # if l_x.size>0 and l_y.size>0 and r_x.size>0 and r_y.size>0:
    #     left_fit = np.polyfit(l_y, l_x, 2)
    #     right_fit = np.polyfit(r_y, r_x, 2)
        
    
    #     # Find the x and y coordinates of all the nonzero 
    #     # (i.e. white) pixels in the frame.         
    #     # nonzero = self.warped_frame.nonzero()  
    #     # nonzeroy = np.array(nonzero[0])
    #     # nonzerox = np.array(nonzero[1])
            
    #     # Store left and right lane pixel indices
    #     left_lane_inds = ((nonz_x > (left_fit[0]*(nonz_y**2) + left_fit[1]*nonz_y + left_fit[2] - margin)) &
    #                     (nonz_x < (left_fit[0]*(nonz_y**2) + left_fit[1]*nonz_y + left_fit[2] + margin))) 
    #     right_lane_inds = ((nonz_x > (right_fit[0]*(nonz_y**2) + right_fit[1]*nonz_y + right_fit[2] - margin)) &
    #                     (nonz_x < (right_fit[0]*(nonz_y**2) + right_fit[1]*nonz_y + right_fit[2] + margin)))           
    
    #     # Get the left and right lane line pixel locations  
    #     leftx = nonz_x[left_lane_inds]
    #     lefty = nonz_y[left_lane_inds] 
    #     rightx = nonz_x[right_lane_inds]
    #     righty = nonz_y[right_lane_inds]    
        
    #     # Fit a second order polynomial curve to each lane line
    #     left_fit = np.polyfit(lefty, leftx, 2)
    #     right_fit = np.polyfit(righty, rightx, 2)
        
    #     # Create the x and y values to plot on the image
    #     ploty = np.linspace(0, warped_image.shape[0]-1, warped_image.shape[0]) 
    #     left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    #     right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
        
    #     out_img = np.dstack((warped_image, warped_image, (warped_image)))*255
    #     window_img = np.zeros_like(out_img)
                
    #     # Add color to the left and right line pixels
    #     # out_img[nonz_y[left_lane_inds], nonz_x[left_lane_inds]] = [255, 0, 0]
    #     # out_img[nonz_y[right_lane_inds], nonz_x[right_lane_inds]] = [0, 0, 255]
        
    #     # Create a polygon to show the search window area, and recast 
    #     # the x and y points into a usable format for cv.fillPoly()
    #     left_line_window1 = np.array([np.transpose(np.vstack([left_fitx-margin, ploty]))])
    #     left_line_window2 = np.array([np.flipud(np.transpose(np.vstack([left_fitx+margin, ploty])))])
    #     left_line_pts = np.hstack((left_line_window1, left_line_window2))
    #     right_line_window1 = np.array([np.transpose(np.vstack([right_fitx-margin, ploty]))])
    #     right_line_window2 = np.array([np.flipud(np.transpose(np.vstack([right_fitx+margin, ploty])))])
    #     right_line_pts = np.hstack((right_line_window1, right_line_window2))
                
    #     # Draw the lane onto the warped blank image
    #     cv.fillPoly(window_img, np.int_([left_line_pts]), (0,255, 0))
    #     cv.fillPoly(window_img, np.int_([right_line_pts]), (0,255, 0))
    #     result = cv.addWeighted(out_img, 1, window_img, 0.3, 0)
        
    #     # Plot the figures 
    #     figure, (ax1, ax2, ax3) = plt.subplots(3,1) # 3 rows, 1 column
    #     figure.set_size_inches(10, 10)
    #     figure.tight_layout(pad=3.0)
    #     ax1.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    #     ax2.imshow(warped_image, cmap='gray')
    #     ax3.imshow(result)
    #     ax3.plot(left_fitx, ploty, color='yellow')
    #     ax3.plot(right_fitx, ploty, color='yellow')
    #     ax1.set_title("Original Frame")  
    #     ax2.set_title("Warped Frame")
    #     ax3.set_title("Warped Frame With Search Window")
    #     plt.show()
        
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