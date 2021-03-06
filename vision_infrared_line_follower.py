import cv2
import numpy as np
from motor import Robot
import time
from timeit import default_timer as timer
from gpiozero import Button, LineSensor
from signal import pause
from motor import Robot
import time

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
    do_otsu = False
    if(do_otsu):
        ret, thresh_frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thresh_frame = np.invert(thresh_frame)
        #ret, thresh_frame = cv2.threshold(gray_frame, 60, 255, cv2.THRESH_BINARY_INV)
    else:
        thresh_frame = frame.copy()
        thresh = 60
        white_pixels = thresh_frame <= thresh
        black_pixels = thresh_frame > thresh
        thresh_frame[white_pixels] = 255
        thresh_frame[black_pixels] = 0
        frame = thresh_frame

    #midpoints = np.zeros((frame.shape[1]))

    '''black_stripe = np.argwhere(thresh_frame == 0)
    for y in range(frame.shape[1]):
        horiz_stripe = np.argwhere(thresh_frame[y,:] == 0)
        if(horiz_stripe.size > 0):
            min_x_stripe = np.min(horiz_stripe)
            max_x_stripe = np.max(horiz_stripe)
            midpoint = min_x_stripe+((max_x_stripe-min_x_stripe)//2)
            thresh_frame[y, midpoint-5:midpoint+5] = 127
            midpoints[y] = midpoint
        else:
            midpoints[y] = -1'''
    midpoints = None
    return thresh_frame, midpoints


def process_capture(capture, show_frame, robot):
    left_sensor = Button(14)
    right_sensor = Button(15)
    
    last_step = timer()
    current_time = timer()
    
    while(capture.isOpened()):
        current_time = timer()
        ret, frame = capture.read()
        frame = cv2.resize(frame, (400, 400))
        
        if(left_sensor.is_pressed and not right_sensor.is_pressed):
            print('infrared right')
            robot.right_curve()
        elif(not left_sensor.is_pressed and right_sensor.is_pressed):
            print('infrared left')
            robot.left_curve()
        elif(not left_sensor.is_pressed and not right_sensor.is_pressed):
            print('infrared forward')
            robot.forward()
        elif(left_sensor.is_pressed and right_sensor.is_pressed):
                    
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame, (5,5), 0)
            
            
            lower_black = np.array([0,0,0])
            upper_black = np.array([80,255,70])
            
            
            segmented_image, line_midpoints = segment_image(gray_frame)
            contours,hierarchy = cv2.findContours(segmented_image.copy(), 1, cv2.CHAIN_APPROX_NONE)
        
        
            if(len(contours) > 0):
                debug = False

                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                if(M['m00'] == 0.0):
                    if(debug):
                        print('Didn\'t detect anything. forward')
                    else:
                        robot.forward()
                    continue
                
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
                cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)
                
                rows, cols = frame.shape[:2]
                [vx, vy, x, y] = cv2.fitLine(c, cv2.DIST_L2, 0, 0.01, 0.01)
                
                lefty = int((-x*vy/vx)+y)
                righty = int((cols-x)*vy/vx+y)
                cv2.line(frame,(cols-1,righty),(0,lefty),(0,255,0),2)
                #cv2.drawContours(frame, contours, -1, (0,255,0), 1)
                
                last_step = timer()
                frame_center = frame.shape[1]/2
            
                if(cx < frame_center-(frame_center/4)):
                    print('vision left')
                    robot.left()
                elif(cx > frame_center+(frame_center/4)):
                    print('vision right')
                    robot.right()
                else:
                    print('vision forward')
                    robot.forward()
         
        
        if(show_frame):
            cv2.imshow('Capture', frame)
                #print('hiding frame')

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
    time.sleep(6)
    print('waking up')

    robot.set_speed(1.0)
    
    capture = start_video_capture(0)
    process_capture(capture, True, robot)
    kill_video_capture(capture)

if __name__ == '__main__':
    main()
