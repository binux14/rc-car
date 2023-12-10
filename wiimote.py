import cwiid
import time
from oled import *
import threading

TIME_CHECK_WIIMOTE = 1000
wm = None
button_state = None

def wiimote_start():	
	x = threading.Thread(target=check_wiimote_connection, args=())
	x.start()
	y = threading.Thread(target=button_state_loop, args=())
	y.start()

def wiimote_connect():
	global wm

	print("Press buttons 1 & 2 at the same time")
	time.sleep(2)
	wm = None
	while not wm:
		try:
			wm = cwiid.Wiimote()
			time.sleep(0.5)
		except RuntimeError:
			print("Could not connect, retrying...")
			time.sleep(1)

	print("Connected to Wiimote")
	wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
	wm.led = 15

def is_wiimote_connected():
	return wm != None

def get_button_state():
	return button_state

def button_state_loop():
	global button_state

	while(True):
		time.sleep(0.01)
		try:
			button_state = wm.state['buttons']
		except:
			pass

def set_wiimote_leds(l):
    wm.led = l

def check_wiimote_connection():
	tw = time.time()*1000
	while(True):
		if(time.time()*1000 - tw > TIME_CHECK_WIIMOTE):
            #for i in range(0,4):
            #	print("MOTOR ", end="")
            #	print(i, end="")
            #	print(": ", end="")
            #	print(int((motor[i][0].duty_cycle)), end="")
            #	print(" | ", end="")
            #	print(int(motor[i][1].duty_cycle))
            #print("******************")
			tw = time.time()*1000
			try:
				set_wiimote_leds(15)
			except AttributeError as e:
				print(e)
				print("Controller disconnected, trying to reconnect...")
				#starts the dynamic connecting screen
				start_wiimote_screen()
				wiimote_connect()
				#stops the dynamic connecting screen
				stop_wiimote_screen()
				time.sleep(0.1)
				
				#shows the checkmark
				clear_display()
				display_show_ok()
				time.sleep(1)

				#Shows the logo
				clear_display()
				display_show_logo()
			except:
				print("Unknown wiimote exception")