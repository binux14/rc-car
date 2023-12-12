from board import SCL, SDA
import busio
import adafruit_pca9685
import time
from wiimote import *
import threading
from sensor_distance import get_distance_state

SPEED_PERCENTAGE = 75
COMP_FACTOR = 0.8

def init_motors():
    global motor
    i2c = busio.I2C(SCL, SDA)
    pca = adafruit_pca9685.PCA9685(i2c)

    pca.frequency = 30

    motor = [[pca.channels[0], pca.channels[1]], [pca.channels[2], pca.channels[3]], [pca.channels[5], pca.channels[4]], [pca.channels[6], pca.channels[7]]]
    motors_run(0,0,False,0)
    motors_start_thread()

def motors_running():
    for i in range(0,4):
        if(motor[i][0].duty_cycle > 0 or motor[i][1].duty_cycle > 0):
            return True
    return False
    

def motors_run(dc, dir, turn, turn_dir):
    dutyc = (dc*0xffff)/100
    dutyc = int(dutyc)
    for i in range(0,4):
        if dir >= 1:
            if(not turn):
                #Motor compensation for straight line driving
                if (i == 1 or i == 3):
                    motor[i][0].duty_cycle = int(dutyc*COMP_FACTOR)
                else:
                    motor[i][0].duty_cycle = dutyc
            else:
                if(turn_dir >= 1):
                    if(i == 1 or i == 3):
                        motor[i][0].duty_cycle = 0
                    else:
                        motor[i][0].duty_cycle = 0xffff
                else:
                    if(i == 0 or i == 2):
                        motor[i][0].duty_cycle = 0
                    else:
                        motor[i][0].duty_cycle = 0xffff
            motor[i][1].duty_cycle = 0
        else:
            if(not turn):
                #Motor compensation for straight line driving
                if (i == 1 or i == 3):
                    motor[i][1].duty_cycle = int(dutyc*COMP_FACTOR)
                else:
                    motor[i][1].duty_cycle = dutyc
            else:
                if(turn_dir >= 1):
                    if(i == 1 or i == 3):
                        motor[i][1].duty_cycle = 0
                    else:
                        motor[i][1].duty_cycle = 0xffff
                else:
                    if(i == 0 or i == 2):
                        motor[i][1].duty_cycle = 0
                    else:
                        motor[i][1].duty_cycle = 0xffff
            motor[i][0].duty_cycle = 0

def motors_brake():
	for i in range(0,4):
		motor[i][0].duty_cycle = 0xffff
		motor[i][1].duty_cycle = 0xffff
	pass

def motors_start_thread():
	x = threading.Thread(target=motors_thread, args=())
	x.start()

def motor_thread_stop():
    global stopThread
    stopThread = True

def motors_thread():
    global stopThread
    stopThread = False
    old_dist_state = 0
    old_state = None
    tw = time.time()*1000
    while(True):
        try:
            if(stopThread):
                sys.exit()
            time.sleep(0.001)
            if(old_dist_state != get_distance_state()):
                old_dist_state = get_distance_state()
                if(old_dist_state == 0):
                        print("OBJECT IN FRONT, STOPPING")
                        if(motors_running()):
                            motors_brake()
                            time.sleep(1)
            elif(old_state != get_button_state()):
                old_state = get_button_state()
                if(old_state & cwiid.BTN_2 & (old_dist_state != 0)):
                    print("FWD - ", end="")
                    if(old_state & cwiid.BTN_UP):
                        print("LEFT")
                        motors_run(SPEED_PERCENTAGE, 0, True, 1)
                    elif(old_state & cwiid.BTN_DOWN):
                        print("RIGHT")
                        motors_run(SPEED_PERCENTAGE, 0, True, 0)
                    else:
                        print("STRAIGHT")
                        motors_run(SPEED_PERCENTAGE, 0, False, 0)
                elif(old_state & cwiid.BTN_1):
                    print("BWD - ", end="")
                    if(old_state & cwiid.BTN_UP):
                        print("LEFT")
                        motors_run(SPEED_PERCENTAGE, 1, True, 1)
                    elif(old_state & cwiid.BTN_DOWN):
                        print("RIGHT")
                        motors_run(SPEED_PERCENTAGE, 1, True, 0)
                    else:
                        print("STRAIGHT")
                        motors_run(SPEED_PERCENTAGE, 1, False, 0)
                else:
                    #print("OFF")
                    motors_run(0, 0, False, 0)
        except AttributeError as e:
            motors_run(0,0,False,0)
            print(e)
            print("Motors: waiting for wiimote to connect")
            while(not is_wiimote_connected()):
                  time.sleep(0.1)
            time.sleep(0.5)
