import cv2
import numpy as np
from motor import Robot
import time
from timeit import default_timer as timer


def load_board_setup():
    configs = {}
    with open('board_setup.cfg') as f:
        content = f.read()
        configs = content.split('\n')
        configs = [x.split('=') for x in configs]
        print(configs)

        config_dict = {}
        for key, value in configs:
            config_dict[key] = value
        return config_dict

def start_video_capture(source):
    capture = cv2.VideoCapture(source)
    return capture

def kill_video_capture(capture):
    capture.release()
    cv2.destroyAllWindows()

def apply_hough_transform(frame):
    line_frame = frame.copy()
    lines = cv2.HoughLines(frame, 1, np.pi/180, 1)
    if(lines is not None):
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(line_frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
    
    return line_frame

def detect_blobs(frame):
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = False
    params.filterByInertia = False
    params.filterByConvexity = True

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(frame)
    #print(keypoints)
    for marker in keypoints:
        kp_frame = cv2.drawMarker(frame, tuple(int(i) for i in marker.pt), color=(0, 255, 0))
    return kp_frame

def segment_image(frame):
    do_otsu = True
    if(do_otsu):
        ret, thresh_frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thresh_frame = np.invert(thresh_frame)
        #ret, thresh_frame = cv2.threshold(gray_frame, 60, 255, cv2.THRESH_BINARY_INV)
    else:
        thresh_frame = frame.copy()
        thresh = 140
        white_pixels = thresh_frame > thresh
        black_pixels = thresh_frame <= thresh
        thresh_frame[white_pixels] = 255
        thresh_frame[black_pixels] = 0
        frame = thresh_frame

    midpoints = np.zeros((frame.shape[1]))

    black_stripe = np.argwhere(thresh_frame == 0)
    for y in range(frame.shape[1]):
        horiz_stripe = np.argwhere(thresh_frame[y,:] == 0)
        if(horiz_stripe.size > 0):
            min_x_stripe = np.min(horiz_stripe)
            max_x_stripe = np.max(horiz_stripe)
            midpoint = min_x_stripe+((max_x_stripe-min_x_stripe)//2)
            thresh_frame[y, midpoint-5:midpoint+5] = 127
            midpoints[y] = midpoint
        else:
            midpoints[y] = -1

    return thresh_frame, midpoints


def process_capture(capture, show_frame, robot):
    last_step = timer()
    current_time = timer()
    
    while(capture.isOpened()):
        current_time = timer()
        
        ret, frame = capture.read()
        frame = cv2.resize(frame, (400, 400))
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (5,5), 0)
        
        segmented_image, line_midpoints = segment_image(gray_frame)
        contours,hierarchy = cv2.findContours(segmented_image.copy(), 1, cv2.CHAIN_APPROX_NONE)
        
        frame_center = frame.shape[0]/2
        if(len(contours) > 0):
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)
            #cv2.drawContours(frame, contours, -1, (0,255,0), 1)
            
            if(current_time - last_step > 0.2):
                last_step = timer() 
                print('cx',cx)
                if(cx < frame_center-(frame_center/4)):
                    print('turn left')
                    robot.left()
                    time.sleep(0.4)
                elif(cx > frame_center+(frame_center/4)):
                    print('turn right')
                    robot.right()
                    time.sleep(0.4)
                else:
                    print('forward')
                    robot.forward()
            else:
                robot.stop()
            
        '''y_lowest_midpoint = int(line_midpoints[line_midpoints != -1].shape[0])
        x_lowest_midpoint = int(line_midpoints[y_lowest_midpoint-1])
        
        y_highest_midpoint = int(line_midpoints[line_midpoints != -1][0])
        x_highest_midpoint = int(line_midpoints[y_highest_midpoint])
        
        frame[segmented_image == 0, 0] = 0
        frame[segmented_image == 0, 1] = 255
        frame[segmented_image == 0, 2] = 0
        frame[segmented_image == 127, :] = 255#Destaca o ponto medio
        
        frame[y_lowest_midpoint-5:y_lowest_midpoint-1, x_lowest_midpoint-5:x_lowest_midpoint-1, :] = [255, 0, 0]
        frame[y_highest_midpoint-5:y_highest_midpoint-1, x_highest_midpoint-5:x_highest_midpoint-1, :] = [255, 0, 0]
        '''
        

        if(show_frame):
            #cv2.imshow('Capture', frame)
            print('hiding frame')

        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

def main():
    robot = Robot(2, 3, 4,
              17, 27, 22,
              26, 19, 5,
              6, 13, 0)
    robot.stop()
    #config_dict = load_board_setup()
    #setup_pins(config_dict)
    print('sleeping')
    time.sleep(10)
    print('waking up')

    robot.set_speed(0.8)
    
    capture = start_video_capture(0)
    process_capture(capture, True, robot)
    kill_video_capture(capture)

if __name__ == '__main__':
    main()