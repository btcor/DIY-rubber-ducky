import usb_hid
import board
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from time import sleep

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
button = digitalio.DigitalInOut(board.GP13)
button.switch_to_input(pull=digitalio.Pull.DOWN)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# Disctionary mapping all keycodes
keycodes = {'A': Keycode.A,
            'B': Keycode.B,
            'C': Keycode.C,
            'D': Keycode.D,
            'E': Keycode.E,
            'F': Keycode.F,
            'G': Keycode.G,
            'H': Keycode.H,
            'I': Keycode.I,
            'J': Keycode.J,
            'K': Keycode.K,
            'L': Keycode.L,
            'M': Keycode.M,
            'N': Keycode.N,
            'O': Keycode.O,
            'P': Keycode.P,
            'Q': Keycode.Q,
            'R': Keycode.R,
            'S': Keycode.S,
            'T': Keycode.T,
            'U': Keycode.U,
            'V': Keycode.V,
            'W': Keycode.W,
            'X': Keycode.X,
            'Y': Keycode.Y,
            'Z': Keycode.Z,
            'n1': Keycode.ONE,
            'n2': Keycode.TWO,
            'n3': Keycode.THREE,
            'n4': Keycode.FOUR,
            'n5': Keycode.FIVE,
            'n6': Keycode.SIX,
            'n7': Keycode.SEVEN,
            'n8': Keycode.EIGHT,
            'n9': Keycode.NINE,
            'n0': Keycode.ZERO,
            'ENTER': Keycode.ENTER,
            'RETURN': Keycode.RETURN,
            'ESCAPE': Keycode.ESCAPE,
            'BACKSPACE': Keycode.BACKSPACE,
            'TAB': Keycode.TAB,
            'SPACE': Keycode.SPACEBAR,
            'n-': Keycode.MINUS,
            'n=': Keycode.EQUALS,
            'n(': Keycode.LEFT_BRACKET,
            'n)': Keycode.RIGHT_BRACKET,
            'n\\': Keycode.BACKSLASH,
            'n#': Keycode.POUND,
            'n;': Keycode.SEMICOLON,
            'QUOTE': Keycode.QUOTE,
            'n`': Keycode.GRAVE_ACCENT,
            'n,': Keycode.COMMA,
            'n.': Keycode.PERIOD,
            'n/': Keycode.FORWARD_SLASH,
            'CAPS_LOCK': Keycode.CAPS_LOCK,
            'F1': Keycode.F1,
            'F2': Keycode.F2,
            'F3': Keycode.F3,
            'F4': Keycode.F4,
            'F5': Keycode.F5,
            'F6': Keycode.F6,
            'F7': Keycode.F7,
            'F8': Keycode.F8,
            'F9': Keycode.F9,
            'F10': Keycode.F10,
            'F11': Keycode.F11,
            'F12': Keycode.F12,
            'PS': Keycode.PRINT_SCREEN,
            'SCROLL_LOCK': Keycode.SCROLL_LOCK,
            'PAUSE': Keycode.PAUSE,
            'INSERT': Keycode.INSERT,
            'HOME': Keycode.HOME,
            'PAGE_UP': Keycode.PAGE_UP,
            'DELETE': Keycode.DELETE,
            'END': Keycode.END,
            'PAGE_DOWN': Keycode.PAGE_DOWN,
            'RIGHT': Keycode.RIGHT_ARROW,
            'LEFT': Keycode.LEFT_ARROW,
            'DOWN': Keycode.DOWN_ARROW,
            'n*': Keycode.KEYPAD_ASTERISK,
            'n+': Keycode.KEYPAD_PLUS,
            'CONTROL': Keycode.CONTROL,
            'SHIFT': Keycode.SHIFT,
            'ALT': Keycode.ALT,
            'OPTION': Keycode.OPTION,
            'META': Keycode.GUI,
            'WINDOWS': Keycode.WINDOWS,
            'COMMAND': Keycode.COMMAND,
            'RIGHT_CONTROL': Keycode.RIGHT_CONTROL,
            'RIGHT_SHIFT': Keycode.RIGHT_SHIFT,
            'RIGHT_ALT': Keycode.RIGHT_ALT,
            'UP': Keycode.UP_ARROW,
            'NUMLOCK': Keycode.KEYPAD_NUMLOCK,
            'MENU': Keycode.APPLICATION,
            'POWER': Keycode.POWER
            }

# Interpret DuckyScript and translate it to keycodes
def ducky(line):
    command = line.split()
    defaultdelay = 0
    
    if command[0] == "REM":
        return   
    elif command[0] == "DEFAULT_DELAY" or command[0] == "DEFAULTDELAY":
        defaultdelay = float(command[1]/1000)
    elif command[0] == "DELAY":
        sleep(float(command[1])/1000)
    elif command[0] == "GUI" or command[0] == "WINDOWS":
        kbd.press(Keycode.WINDOWS)
        if len(command) > 1:
            for c in command[1:]:
                kbd.press(keycodes[c.upper()])
        kbd.release_all()
    elif command[0] == "MENU" or command[0] == "APP":
        kbd.send(Keycode.APPLICATION)
    elif command[0] == "SHIFT":
        kbd.press(Keycode.SHIFT)
        if len(command) > 1:
            for c in command[1:]:
                kbd.press(c)   
        kbd.release_all()
    elif command[0] == "ALT":
        kbd.press(Keycode.ALT)
        if len(command) > 1:
            for c in command[1:]:
                kbd.press(c)
        kbd.release_all()
    elif command[0] == "CONTROL" or command[0] == "CTRL":
        kbd.press(Keycode.CONTROL)
        if len(command) > 1:
            for i in range(1, len(command)):
                kbd.press(command[i])   
        kbd.release_all()
    elif command[0] == "STRING":
        for c in command[1:]:
            layout.write(c + ' ')
    else:
        kbd.send(keycodes[command[0]])
        
# If button pressed, blink LED and do not run payload
if button.value:
    print("button pressed")
    while(True):
        led.value = True
        sleep(.5)
        led.value = False
        sleep(.5)
else:
    print("button not pressed")
    # payload.txt must be a ducky script file
    with open("payload.txt") as f:
        lines = f.read().splitlines()
        for line in lines:
            ducky(line)