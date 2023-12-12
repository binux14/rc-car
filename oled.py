import adafruit_ssd1306
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import threading
import time
import sys
import busio
import board

IMAGE_LOGO_PATH = '/home/rccar/rc-car/images/land_rover.bmp'
IMAGE_WELCOME_PATH = '/home/rccar/rc-car/images/rccar.bmp'
IMAGE_OK_PATH = '/home/rccar/rc-car/images/ok.bmp'
IMAGE_NOPE_PATH = '/home/rccar/rc-car/images/nope.bmp'

FONT_PATH = '/home/rccar/rc-car/Roboto-Medium.ttf'
FONT_TITLE = 2
FONT_REG = 1
FONT_SMALL = 0

wiimoteConnecting = False

def init_oled():
	global font_title, font_reg, font_small, draw, disp, image, image_ok, image_logo, image_welcome, image_nope

	# Raspberry Pi pin configuration:
	RST = 24

	i2c = busio.I2C(board.SCL, board.SDA)

	# 128x64 display with hardware I2C:
	disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

	# Initialize library.
	#disp.begin()

	# Clear display.
	disp.fill(0)
	disp.show()

	# Create blank image for drawing.
	# Make sure to create image with mode '1' for 1-bit color.
	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))

	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)
	image_ok = Image.open(IMAGE_OK_PATH).convert('1')
	image_logo = Image.open(IMAGE_LOGO_PATH).convert('1')
	image_welcome = Image.open(IMAGE_WELCOME_PATH).convert('1')
	image_nope = Image.open(IMAGE_NOPE_PATH).convert('1')

	# Draw a black filled box to clear the image.
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	# Load default font.
	#font = ImageFont.load_default()

	# Alternatively load a TTF font.  Make sure the .ttf font file is in th># Some other nice fonts to try: http://www.dafont.com/bitmap.php
	font_title = ImageFont.truetype(FONT_PATH, 48)
	font_reg = ImageFont.truetype(FONT_PATH, 18)
	font_small = ImageFont.truetype(FONT_PATH, 14)

	# Display image.
	disp.image(image)
	disp.show()

def clear_display():
	draw.rectangle((0,0,128,64), fill=0)

#Used internally only
def display_show(im):
    disp.image(im)
    disp.show()

def draw_multiline(str, size):
	if(size == 0):
		draw.multiline_text((64, 32), str, anchor="mm", align="center", font=font_small, fill=255)
	elif(size == 1):
		draw.multiline_text((64, 32), str, anchor="mm", align="center", font=font_reg, fill=255)
	else:
		draw.multiline_text((64, 32), str, anchor="mm", align="center", font=font_title, fill=255)
	display_show(image)

def display_show_ok():
	disp.image(image_ok)
	disp.show()

def show_welcome_screen():
	disp.image(image_welcome)
	disp.show()

def display_show_logo():
	disp.image(image_logo)
	disp.show()

def display_show_nope():
	disp.image(image_nope)
	disp.show()

def start_wiimote_screen():
	global exitWiimoteScreen
	exitWiimoteScreen = False
	x = threading.Thread(target=wiimote_screen_loop, args=())
	x.start()

def stop_wiimote_screen():
	global exitWiimoteScreen
	exitWiimoteScreen = True

def wiimote_screen_loop():
	global exitWiimoteScreen
	state = 0
	while(True):
		clear_display()
		if(state == 0):
			draw_multiline("Connecting to\nWiimote\nPress buttons 1 + 2", FONT_SMALL)
			state = 1
		elif(state == 1):
			draw_multiline("Connecting to\nWiimote.\nPress buttons 1 + 2", FONT_SMALL)
			state = 2
		elif(state == 2):
			draw_multiline("Connecting to\nWiimote..\nPress buttons 1 + 2", FONT_SMALL)
			state = 3
		elif(state == 3):
			draw_multiline("Connecting to\nWiimote...\nPress buttons 1 + 2", FONT_SMALL)
			state = 0
		time.sleep(0.25)
		if(exitWiimoteScreen):
			sys.exit()
