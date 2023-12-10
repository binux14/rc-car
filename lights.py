import board
import neopixel
from rpi_ws281x import Color
import threading
import time
from wiimote import *
import cwiid

NUM_LEDS = 6

RED = Color(255,0,0)
GREEN = Color(0,255,0)
BLUE = Color(0,0,255)
WHITE = Color(255,255,255)
BLACK = Color(0,0,0)
YELLOW = Color(255,255,0)

BLINKERS_COLOR = Color(13, 13, 0)
HEADLIGHTS_COLOR = Color(13,13,6)
HIGHBEAMS_COLOR = Color(255,255,127)

BRIGHTNESS = 1

HAZARDS_TIME_S = 0.4

def init_lights():
    global pixels, h_on, state, highbeams_on

    state = 0
    highbeams_on = False
    h_on = False
    pixels = neopixel.NeoPixel(board.D18, NUM_LEDS, auto_write=True)
    pixels.pixel_order = neopixel.GRBW
    pixels.frequency = 6400000
    pixels.brightness = BRIGHTNESS
    pixels.fill(BLACK)
    m = threading.Thread(target=blinkers_thread, args=())
    m.start()
    n = threading.Thread(target=lights_loop, args=())
    n.start()

def set_headlights(head_on):
    for i in range(1,5):
            if(head_on):
                pixels[i] = HEADLIGHTS_COLOR
            else:
                pixels[i] = BLACK
     
def set_hazards(h_state):
    global h_on
    h_on = h_state

def blinkers_thread():
    global h_on, state
    while(True):
        time.sleep(0.01)
        if(h_on):
            if(state == 0):
                state = 1
                pixels[0] = BLINKERS_COLOR
                pixels[5] = BLINKERS_COLOR
            else:
                state = 0
                pixels[0] = BLACK
                pixels[5] = BLACK

def set_high_beams(hb_on):
    global highbeams_on
    highbeams_on = hb_on
    for i in range(1,5):
        if(highbeams_on):
            pixels[i] = HIGHBEAMS_COLOR
        else:
            pixels[i] = HEADLIGHTS_COLOR

def lights_loop():
    global h_on, highbeams_on
    old_state = None
    new_state = None

    while(True):
        try:
            time.sleep(0.01)
            new_state = get_button_state()
            if(old_state != new_state):
                print("STATE CHANGE!")
                old_state = new_state
                if(new_state & cwiid.BTN_B):
                    set_high_beams(True)
                else:
                    set_high_beams(False)
        except:
            pass