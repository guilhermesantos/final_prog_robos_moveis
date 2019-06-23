from gpiozero import LED, PWMLED
import time
import curses

class Robot():
    def __init__(self, motor1_a, motor1_b, motor1_spd_pin,
                 motor2_a, motor2_b, motor2_spd_pin,
                 motor3_a, motor3_b, motor3_spd_pin,
                 motor4_a, motor4_b, motor4_spd_pin):
        self.down_left_a = LED(motor1_a)
        self.down_left_b = LED(motor1_b)
        self.down_left_spd_pin = PWMLED(motor1_spd_pin)
        
        self.down_right_a = LED(motor2_a)
        self.down_right_b = LED(motor2_b)
        self.down_right_spd_pin = PWMLED(motor2_spd_pin)
        
        self.up_right_motor_a = LED(motor3_a)
        self.up_right_motor_b = LED(motor3_b)
        self.up_right_motor_spd_pin = PWMLED(motor3_spd_pin)
        
        self.up_left_motor_a = LED(motor4_a)
        self.up_left_motor_b = LED(motor4_b)
        self.up_left_motor_spd_pin = PWMLED(motor4_spd_pin)
        
        self.spd = 1.0
        self.down_left_spd_pin.value = self.spd
        self.down_right_spd_pin.value = self.spd
        self.up_right_motor_spd_pin.value = self.spd
        self.up_left_motor_spd_pin.value = self.spd
        
                
    def forward(self):
        self.down_left_a.on()
        self.down_left_b.off()
        
        self.down_right_a.off()
        self.down_right_b.on()
        
        self.up_right_motor_a.off()
        self.up_right_motor_b.on()
        
        self.up_left_motor_a.off()
        self.up_left_motor_b.on()
        
        self.down_left_spd_pin.value = self.spd
        self.down_right_spd_pin.value = self.spd
        self.up_right_motor_spd_pin.value = self.spd
        self.up_left_motor_spd_pin.value = self.spd        
    
    def left(self):
        self.down_left_a.off()
        self.down_left_b.on()
        
        self.down_right_a.off()
        self.down_right_b.on()
        
        self.up_right_motor_a.off()
        self.up_right_motor_b.on()
        
        self.up_left_motor_a.on()
        self.up_left_motor_b.off()
        
        self.down_left_spd_pin.value = self.spd
        self.down_right_spd_pin.value = self.spd
        self.up_right_motor_spd_pin.value = self.spd
        self.up_left_motor_spd_pin.value = self.spd  
            
    def right(self):
        self.down_left_a.on()
        self.down_left_b.off()
        
        self.down_right_a.on()
        self.down_right_b.off()
        
        self.up_right_motor_a.on()
        self.up_right_motor_b.off()
        
        self.up_left_motor_a.off()
        self.up_left_motor_b.on()
        
        self.down_left_spd_pin.value = self.spd
        self.down_right_spd_pin.value = self.spd
        self.up_right_motor_spd_pin.value = self.spd
        self.up_left_motor_spd_pin.value = self.spd  
        
    def backwards(self):
        self.down_left_a.off()
        self.down_left_b.on()
        
        self.down_right_a.on()
        self.down_right_b.off()
        
        self.up_right_motor_a.on()
        self.up_right_motor_b.off()
        
        self.up_left_motor_a.on()
        self.up_left_motor_b.off()
        
        self.down_left_spd_pin.value = self.spd
        self.down_right_spd_pin.value = self.spd
        self.up_right_motor_spd_pin.value = self.spd
        self.up_left_motor_spd_pin.value = self.spd  
        
    def stop(self):
        self.down_left_a.off()
        self.down_left_b.off()
        
        self.down_right_a.off()
        self.down_right_b.off()
        
        self.up_right_motor_a.off()
        self.up_right_motor_b.off()
        
        self.up_left_motor_a.off()
        self.up_left_motor_b.off()

    def left_curve(self):        
        self.down_left_a.off()
        self.down_left_b.on()
        
        self.down_right_a.off()
        self.down_right_b.on()
        
        self.up_right_motor_a.off()
        self.up_right_motor_b.on()
        
        self.up_left_motor_a.on()
        self.up_left_motor_b.off()
        
        self.down_left_spd_pin.value = self.spd
        self.down_right_spd_pin.value = self.spd * 0.75
        self.up_right_motor_spd_pin.value = self.spd * 0.75
        self.up_left_motor_spd_pin.value = self.spd
    
    def right_curve(self):
        self.down_left_a.on()
        self.down_left_b.off()
        
        self.down_right_a.on()
        self.down_right_b.off()
        
        self.up_right_motor_a.on()
        self.up_right_motor_b.off()
        
        self.up_left_motor_a.off()
        self.up_left_motor_b.on()
        
        self.down_left_spd_pin.value = self.spd * 0.75
        self.down_right_spd_pin.value = self.spd 
        self.up_right_motor_spd_pin.value = self.spd 
        self.up_left_motor_spd_pin.value = self.spd * 0.75

    def set_speed(self, spd):
        self.spd = spd
        self.down_left_spd_pin.value = spd
        self.down_right_spd_pin.value = spd
        self.up_right_motor_spd_pin.value = spd
        self.up_left_motor_spd_pin.value = spd
        
def setup_curses(win):
    curses.noecho()
    curses.cbreak()
    win.keypad(True)
    win.nodelay(True)
    win.clear()
    
def terminate_curses(win):
    curses.nocbreak()
    win.keypad(False)
    curses.echo()
    curses.endwin()

def main(win):
    setup_curses(win)
    robot = Robot(2, 3, 4,
                  17, 27, 22,
                  26, 19, 5,
                  6, 13, 0)
    #spd = 1.0
    robot.set_speed(0.5)
    while(True):
        try:
            key = win.getkey()
            if(key == 'KEY_UP'):
                print('up')
                robot.forward()
            elif(key == 'KEY_LEFT'):
                print('left')
                robot.left()
            elif(key == 'KEY_RIGHT'):
                print('right')
                robot.right()
            elif(key == 'KEY_DOWN'):
                print('down')
                robot.backwards()
            elif(key == 'q'):
                terminate_curses()
                curses.endwin()
                exit()
            elif(key == ' '):
                robot.stop()
            else:
                print(key)
                    
            #if()
            #    robot.right()
            #else:
            #    robot.stop()
        except:
            pass
        #if(spd == 1.0):
        #    spd = 0.35
        #else:
        #    spd = 1.0
    

if __name__ == '__main__':
    curses.wrapper(main)
