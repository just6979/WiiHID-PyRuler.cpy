import gc
import os
import time
import board
import touchio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from digitalio import DigitalInOut, Direction

WINDOWS = "W"
MAC = "M"
LINUX = "L"  # and Chrome OS

# Set your computer type to one of the above
OS = LINUX

print(dir(board), os.uname()) # Print a little about ourselves

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
sensitivity = 33
do_clicks = True
left_down = False
right_down = False

status_led = DigitalInOut(board.LED)
status_led.direction = Direction.OUTPUT

touches = [DigitalInOut(board.CAP0)]
for p in (board.CAP1, board.CAP2, board.CAP3):
    touches.append(touchio.TouchIn(p))

leds = []
for p in (board.LED4, board.LED5, board.LED6, board.LED7):
    led = DigitalInOut(p)
    led.direction = Direction.OUTPUT
    led.value = True
    time.sleep(0.1)
    leds.append(led)
for led in reversed(leds):
    led.value = False
    time.sleep(0.1)

cap_touches = [False, False, False, False]


def read_caps():
    t0_count = 0
    t0 = touches[0]
    t0.direction = Direction.OUTPUT
    t0.value = True
    t0.direction = Direction.INPUT
    # funky idea but we can 'diy' the one non-hardware captouch device by hand
    # by reading the drooping voltage on a tri-state pin.
    t0_count = t0.value + t0.value + t0.value + t0.value + t0.value + \
               t0.value + t0.value + t0.value + t0.value + t0.value + \
               t0.value + t0.value + t0.value + t0.value + t0.value
    cap_touches[0] = t0_count > 2
    cap_touches[1] = touches[1].raw_value > 3000
    cap_touches[2] = touches[2].raw_value > 3000
    cap_touches[3] = touches[3].raw_value > 3000
    return cap_touches


def type_alt_code(code):
    kbd.press(0xE2)  # KEYCODE_ALT
    for c in str(code):
        if c == '0':
            keycode = 0x62  # KEYPAD_ZERO
        elif '1' <= c <= '9':
            keycode = 0x59 + ord(c) - ord('1')  # KEYPAD_ONE
        else:
            continue
        kbd.press(keycode)
        kbd.release(keycode)
    kbd.release_all()

while True:
    caps = read_caps()
    # print(caps)
    # light up the matching LED
    for i, c in enumerate(caps):
        leds[i].value = c
    if caps[0]:
        if OS == WINDOWS:
            type_alt_code(234)
        elif OS == MAC:
            kbd.send(0xE2, 0x1D)  # ALT Z
        elif OS == LINUX:
            kbd.press(0xE0, 0xE1)  # CTRL SHIFT
            kbd.press(0x18)  # U
            kbd.release_all()
            kbd.send(0x1F)  # TWO
            kbd.send(0x1E)  # ONE
            kbd.send(0x1F)  # TWO
            kbd.send(0x23)  # SIX
            kbd.send(0x28)  # ENTER
    if caps[1]:
        if OS == WINDOWS:
            type_alt_code(230)
        elif OS == MAC:
            kbd.send(0xE2, 0x10)  # ALT, M
        elif OS == LINUX:
            kbd.press(0xE0, 0xE1)  # CTRL SHIFT
            kbd.press(0x18)  # U
            kbd.release_all()
            kbd.send(0x27)  # 0
            kbd.send(0x20)  # 3
            kbd.send(0x05)  # B
            kbd.send(0x06)  # C
            kbd.send(0x28)  # ENTER
    if caps[2]:
        if OS == WINDOWS:
            type_alt_code(227)
        elif OS == MAC:
            kbd.send(0xE2, 0x13)  # ALT P
        elif OS == LINUX:
            kbd.press(0xE0, 0xE1)  # CRTL SHIFT
            kbd.press(0x18)  # U
            kbd.release_all()
            kbd.send(0x27)  # 0
            kbd.send(0x20)  # 3
            kbd.send(0x06)  # C
            kbd.send(0x27)  # 0
            kbd.send(0x28)  # ENTER
    if caps[3]:
        if OS == WINDOWS:
            type_alt_code(231)
        elif OS == MAC:
            pass
        elif OS == LINUX:
            kbd.press(0xE0, 0xE1)  # CTRL SHIFT
            kbd.press(0x18)  # U
            kbd.release_all()
            kbd.send(0x27)  # 0
            kbd.send(0x20)  # 3
            kbd.send(0x06)  # C
            kbd.send(0x21)  # 4
            kbd.send(0x28)  # ENTER
    time.sleep(0.1)
