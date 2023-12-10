import time
import cwiid

connected = False

global wm

def isConnected():
    try:
        wm.led = 15
    except AttributeError as e:
        connected = False
        print(e)
        print("Controller disconnected, please reinitialize it")

def get_button():
    if not connected:
        return -1
    return wm.state['buttons']

def init_wiimote():
    #connecting to the Wiimote. This allows several attempts
    # as first few often fail.
    print('Press 1+2 on your Wiimote now...')
    time.sleep(3)

    wm = None
    while not wm:
        try:
            wm=cwiid.Wiimote()
        except RuntimeError:
            print("Controller not found, retrying...")
    print("Connected successfully to Wiimote")
    connected = True
    wm.led = 15 #turn on all LEDs
    wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC #report buttons and accelerometer

init_wiimote()
