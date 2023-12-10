import board
import busio
import adafruit_vl53l0x
import time
import threading
import sys

TIME_CHECK_MS = 100
TIME_DEBUG_MS = 1000
MIN_DIST_MM_LOW = 150
MIN_DIST_MM_HIGH = 200

def init_dist_sensors():
	global distance, sensor, distance_state
	distance = 0
	distance_state = 1

	i2c = busio.I2C(board.SCL, board.SDA)
	sensor = adafruit_vl53l0x.VL53L0X(i2c)

	x = threading.Thread(target=sensor_thread, args=())
	x.start()
	y = threading.Thread(target=sensor_hysteresis_thread, args=())
	y.start()

def get_distance_mm():
	global distance
	return distance

def get_distance_state():
	#0 means motors should stop moving forward, 1 means we are okay
	global distance_state
	try:
		return distance_state
	except:
		return 1

def sensor_thread_stop():
	global threadStop
	threadStop = True

def sensor_thread():
	global distance, sensor, threadStop

	threadStop = False
	tc = 0
	try:
		while(True):
			if(threadStop):
				sys.exit()
			time.sleep(0.01)
			if(time.time()*1000 - tc > TIME_CHECK_MS):
				tc = time.time()*1000
				distance = sensor.range
	except:
		print("Error reading distance sensor")

def sensor_hysteresis_thread():
	global distance_state

	if get_distance_mm() <= MIN_DIST_MM_LOW:
		distance_state = 0
	else:
		distance_state = 1

	td = time.time()*1000
	while(True):
		time.sleep(0.01)
		if distance_state == 0:
			if(get_distance_mm() >= MIN_DIST_MM_HIGH):
				distance_state = 1
		elif distance_state == 1:
			if(get_distance_mm() <= MIN_DIST_MM_HIGH):
				distance_state = 0
			pass
		else:
			print("Sensor state error, thread exiting")
