import time
from motors import *
from wiimote import *
from oled import *
from sensor_distance import *
from lights import *
import neopixel
import os

SW_VERSION = "v0.22"

if __name__ == "__main__":
	try:
		while(True):
			print("Starting RC CAR ", end="")
			print(SW_VERSION)

			#Start streaming
			os.system("sudo python3 /home/rccar/rc-car/camera.py &")

			#init_dist_sensors()

			ligths = Lights(neopixel.NeoPixel(board.D18, NUM_LEDS, auto_write=True))
			ligths.init()

			init_oled()
			time.sleep(0.1)

			show_welcome_screen()
			time.sleep(2)

			wiimote_start()

			#stops the dynamic connecting screen
			stop_wiimote_screen()

			#inits the motor variables and thread
			init_motors()

			while(True):
				time.sleep(0.5)

	except Exception as e:
		print(e)
		stop_wiimote_screen()
		time.sleep(0.1)
		clear_display()
		display_show_nope()
	except KeyboardInterrupt:
		stop_wiimote_screen()
		time.sleep(0.1)
		print("Program manually stopped")
		clear_display()
		display_show_nope()
		motor_thread_stop()
		sensor_thread_stop()
