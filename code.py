import board
import displayio
import terminalio
import microcontroller
import busio
import time
import digitalio
from board import *
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
# comment out these lines for non_US keyboards
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
# uncomment these lines for non_US keyboards
# replace LANG with appropriate language
#from keyboard_layout_win_LANG import KeyboardLayout
#from keycode_win_LANG import Keycode


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


duckyCommands = {
    'WINDOWS': Keycode.WINDOWS, 'GUI': Keycode.GUI,
    'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION, 'SHIFT': Keycode.SHIFT,
    'ALT': Keycode.ALT, 'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL,
    'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
    'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
    'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
    'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
    'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
    'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
    'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
    'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
    'BACKSPACE': Keycode.BACKSPACE,
    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
    'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
    'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
    'F12': Keycode.F12,

}


def convertLine(line):
    newline = []
    # print(line)
    # loop on each key - the filter removes empty values
    for key in filter(None, line.split(" ")):
        key = key.upper()
        # find the keycode for the command in the list
        command_keycode = duckyCommands.get(key, None)
        if command_keycode is not None:
            # if it exists in the list, use it
            newline.append(command_keycode)
        elif hasattr(Keycode, key):
            # if it's in the Keycode module, use it (allows any valid keycode)
            newline.append(getattr(Keycode, key))
        else:
            # if it's not a known key name, show the error for diagnosis
            print(f"Unknown key: <{key}>")
    # print(newline)
    return newline


def runScriptLine(line):
    for k in line:
        kbd.press(k)
    kbd.release_all()


def sendString(line):
    layout.write(line)


def parseLine(line):
    global defaultDelay
    if(line[0:3] == "REM"):
        # ignore ducky script comments
        pass
    elif(line[0:5] == "DELAY"):
        time.sleep(float(line[6:])/1000)
    elif(line[0:6] == "STRING"):
        sendString(line[7:])
    elif(line[0:5] == "PRINT"):
        print("[SCRIPT]: " + line[6:])
    elif(line[0:6] == "IMPORT"):
        runScript(line[7:])
    elif(line[0:13] == "DEFAULT_DELAY"):
        defaultDelay = int(line[14:]) * 10
    elif(line[0:12] == "DEFAULTDELAY"):
        defaultDelay = int(line[13:]) * 10
    elif(line[0:3] == "LED"):
        if(led.value == True):
            led.value = False
        else:
            led.value = True
    else:
        newScriptLine = convertLine(line)
        runScriptLine(newScriptLine)

def getProgrammingStatus():
    # check GP0 for setup mode
    # see setup mode for instructions
    progStatusPin = digitalio.DigitalInOut(GP0)
    progStatusPin.switch_to_input(pull=digitalio.Pull.UP)
    progStatus = not progStatusPin.value
    return(progStatus)


def runScript(file):
    global defaultDelay

    duckyScriptPath = file
    f = open(duckyScriptPath, "r", encoding='utf-8')
    previousLine = ""
    duckyScript = f.readlines()
    for line in duckyScript:
        line = line.rstrip()
        if(line[0:6] == "REPEAT"):
            for i in range(int(line[7:])):
                # repeat the last command
                parseLine(previousLine)
                time.sleep(float(defaultDelay)/1000)
        else:
            parseLine(line)
            previousLine = line
        time.sleep(float(defaultDelay)/1000)


def selectPayload():
    payload = "payload.dd"
    # check switch status
    # payload1 = GPIO4 to GND
    # payload2 = GPIO5 to GND
    # payload3 = GPIO10 to GND
    # payload4 = GPIO11 to GND
    payload1Pin = digitalio.DigitalInOut(GP4)
    payload1Pin.switch_to_input(pull=digitalio.Pull.UP)
    payload1State = not payload1Pin.value
    payload2Pin = digitalio.DigitalInOut(GP5)
    payload2Pin.switch_to_input(pull=digitalio.Pull.UP)
    payload2State = not payload2Pin.value
    payload3Pin = digitalio.DigitalInOut(GP10)
    payload3Pin.switch_to_input(pull=digitalio.Pull.UP)
    payload3State = not payload3Pin.value
    payload4Pin = digitalio.DigitalInOut(GP11)
    payload4Pin.switch_to_input(pull=digitalio.Pull.UP)
    payload4State = not payload4Pin.value

    if(payload1State == True):
        payload = "payload.dd"

    elif(payload2State == True):
        payload = "payload2.dd"

    elif(payload3State == True):
        payload = "payload3.dd"

    elif(payload4State == True):
        payload = "payload4.dd"

    else:
        # if all pins are high, then no switch is present
        # default to payload1
        payload = "payload.dd"

    return payload

def getCpuTemp():
    return (microcontroller.cpu.temperature  * (9/5) + 32) - 0.25

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)
# sleep at the start to allow the device to be recognized by the host computer
time.sleep(.5)
defaultDelay = 0

led.value = True
try:
    from adafruit_display_text import label
    import adafruit_displayio_ssd1306
    displayio.release_displays()
    i2c = busio.I2C (scl=board.GP21, sda=board.GP20)
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

    text_group = displayio.Group()
    text = 'USB Rubber Ducky\nBy OCEAN OF ANYTHING\n\nExecuting Payload.'
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=5, y=5)
    text_group.append(text_area)
    display.show(text_group)
    time.sleep(1)
    text = 'USB Rubber Ducky\nBy OCEAN OF ANYTHING\n\nExecuting Payload..'
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=5, y=5)
    text_group.append(text_area)
    display.show(text_group)
    time.sleep(1)
    text = 'USB Rubber Ducky\nBy OCEAN OF ANYTHING\n\nExecuting Payload...'
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=5, y=5)
    text_group.append(text_area)
    display.show(text_group)
    time.sleep(2)
except Exception as e:
    print(f"Error: {e}")

startTime = time.time()
progStatus = False
progStatus = getProgrammingStatus()

if(progStatus == False):
    # not in setup mode, inject the payload
    payload = selectPayload()
    print("Running ", payload)
    runScript(payload)

    print("Done")
else:
    print("Update your payload")





while True:
    try:
        # Make the display context
        text_group = displayio.Group()
        # Draw a label
        text = '- USB Rubber Ducky -'
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=5, y=5)
        text_group.append(text_area)
        text = "CPU Temp: {:.2f} °F".format(getCpuTemp())
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=18)
        text_group.append(text_area)
        text = "Payload: {}".format(payload)
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=31)
        text_group.append(text_area)
        endTime = time.time()
        temp = endTime - startTime
        hours = (temp//3600)
        temp = (temp - 3600*hours)
        minutes = (temp//60)
        seconds = (temp - 60*minutes)
        newhours = str(hours)
        newminuites = str(minutes)
        newseconds = str(seconds)
        spentTime = newhours+':'+newminuites+':'+newseconds
        text = "Time Spend: {}".format(spentTime)
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=44)
        text_group.append(text_area)
        text = "By OCEAN OF ANYTHING"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=57)
        text_group.append(text_area)
        display.show(text_group)
    except Exception as e:
        print(f"Error: {e}")
    led.value = not led.value
    time.sleep(0.1)