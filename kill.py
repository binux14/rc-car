from board import SCL, SDA
import busio
import adafruit_pca9685
import time

def motors_run(dc, dir):
	dutyc = (dc*0xffff)/100
	dutyc = int(dutyc)
	for i in range(0,6):
		if dir == 0:
			motor[i][0].duty_cycle = dutyc
			motor[i][1].duty_cycle = 0
		else:
			motor[i][0].duty_cycle = 0
			motor[i][1].duty_cycle = dutyc

i2c = busio.I2C(SCL, SDA)
pca = adafruit_pca9685.PCA9685(i2c)

pca.frequency = 30

motor = [[pca.channels[0], pca.channels[1]], [pca.channels[2], pca.channels[3]], [pca.channels[4], pca.channels[5]], [pca.channels[6], pca.channels[7]], [pca.channels[8], pca.channels[9]], [pca.channels[10], pca.channels[11]]]

motors_run(0,0)
