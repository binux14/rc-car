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

BLINKERS_COLOR = Color(26, 26, 0)
HEADLIGHTS_COLOR = Color(13,13,6)
HIGHBEAMS_COLOR = Color(255,255,127)

BRIGHTNESS = 1

HAZARDS_TIME_S = 0.4

class Lights:
    _hazards_on = False
    _right_blinkers_on = False
    _left_blinkers_on = False
    _headlights_on = False
    _blink_state = 0
    _new_button_state = None
    _highbeams_on = False
    _permanent_highbeams = False

    def __init__(self, pixels):
        self._pixels = pixels
        self._pixels.frequency = 6400000
        self._pixels.brightness = BRIGHTNESS
        self._pixels.fill(BLACK)

    def init(self):
        threading.Thread(target=self.blinkers_thread, args=()).start()
        threading.Thread(target=self.lights_loop, args=()).start()

    def set_headlights(self, head_on):
        for i in range(1,5):
                if(head_on):
                    self._pixels[i] = HEADLIGHTS_COLOR
                else:
                    self._pixels[i] = BLACK
        self._headlights_on = head_on
     
    def set_hazards(self, h_state):
        self._hazards_on = h_state

    def blinkers_thread(self):
        while(True):
            time.sleep(HAZARDS_TIME_S)
            if(self._hazards_on):
                if(self._blink_state == 0):
                    self._blink_state = 1
                    self._pixels[0] = BLINKERS_COLOR
                    self._pixels[5] = BLINKERS_COLOR
                else:
                    self._blink_state = 0
                    self._pixels[0] = BLACK
                    self._pixels[5] = BLACK
            else:
                self._pixels[0] = BLACK
                self._pixels[5] = BLACK


    def set_high_beams(self, hb_on):
        self._highbeams_on = hb_on
        for i in range(1,5):
            if(self._highbeams_on):
                self._pixels[i] = HIGHBEAMS_COLOR
            else:
                if(self._headlights_on):
                    self._pixels[i] = HEADLIGHTS_COLOR
                else:
                    self._pixels[i] = BLACK
          
    def long_press_highbeams(self):
        LONG_PRESS_MS = 1000
        t = time.time()*1000
        exit = False

        while(time.time()*1000 - t < LONG_PRESS_MS):
            time.sleep(0.01)
            if(not self._new_button_state & cwiid.BTN_B):
                exit = True
                break
        if(not exit):
            self._permanent_highbeams = True
            self.set_high_beams(False)
            time.sleep(0.01)
            self.set_high_beams(True)
        else:
            self._permanent_highbeams = False
            self.set_high_beams(False)


    def lights_loop(self):
        old_state = None

        while(True):
            try:
                time.sleep(0.01)
                self._new_button_state = get_button_state()
                if(old_state != self._new_button_state):
                    old_state = self._new_button_state
                    print("HEAD: ", end="")
                    print(self._headlights_on)
                    print("HIGH B: ", end="")
                    print(self._highbeams_on)
                    print("HIGH B PERM: ", end="")
                    print(self._permanent_highbeams)
                    if(self._new_button_state & cwiid.BTN_B):
                        self.set_high_beams(True)
                        threading.Timer(0, self.long_press_highbeams, args=()).start()
                    else:
                        if(not self._permanent_highbeams):
                            self.set_high_beams(False)
                    if(self._new_button_state & cwiid.BTN_A):
                        if(self._highbeams_on):
                            self.set_headlights(False)
                            self.set_high_beams(False)
                            self._permanent_highbeams = False
                        elif(self._headlights_on):
                            self.set_headlights(False)
                        else:
                            self.set_headlights(True)
                        pass
                    if(self._new_button_state & cwiid.BTN_PLUS):
                        if(self._hazards_on):
                            self.set_hazards(False)
                        else:
                            self.set_hazards(True)
                        pass
            except Exception as e:
                print("Error handling lights:")
                print(e)
                pass