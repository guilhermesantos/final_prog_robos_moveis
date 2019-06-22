from gpiozero import Button, LineSensor
from signal import pause
from motor import Robot


def main():
    left_sensor = Button(14)
    right_sensor = Button(15)
    #sensor = LineSensor(14)
    #sensor.when_line = lambda: print('achou linha')
    #sensor.when_no_line = lambda: print('nao achou linha')
    #pause()
    while(True):
        if(left_sensor.is_pressed and not right_sensor.is_pressed):
            print('turning right')
            #robot.right()
        elif(not left_sensor.is_pressed and right_sensor.is_pressed):
            print('turning left')
            #robot.left()
        elif(not left_sensor.is_pressed and not right_sensor.is_pressed):
            print('on the line (moving forward)')
            #robot.forward()
        elif(left_sensor.is_pressed and right_sensor.is_pressed):
           print('off of the line (moving forward)')
           #robot.forward()
            
if __name__ == '__main__':
    robot = Robot(2, 3, 4,
              17, 27, 22,
              26, 19, 5,
              6, 13, 0)
    robot.stop()
    main()