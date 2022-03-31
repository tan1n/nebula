import numpy as np
import cv2
from time import sleep, time
import mss
import serial
import mss.tools

start_tine = time()
frame = 0

resolution = (1920, 1080)
factor = 10

dimensions = [
    [{"top": 10, "left": 10, "width": 1910, "height": 1}, 'top'],  # top
    [{"top": 10, "left": 1910, "width": 1, "height": 1070}, 'right'],  # right
    [{"top": 1070, "left": 10, "width": 1910, "height": 1}, 'bottom'],  # bottom
    [{"top": 10, "left": 10, "width": 1, "height": 1070}, 'left']  # left
]

led_width = 20
led_height = 13


def capture(args):
    res = (led_width, 1) if args[1] == 'top' or args[1] == 'bottom' else (
        1, led_height)
    with mss.mss() as sct:
        screen = np.array(sct.grab(args[0]))
        img = cv2.resize(screen, res,
                         interpolation=cv2.INTER_NEAREST)
        output = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return np.array(output).flatten().tolist()


def write(data, link):
    for x, i in enumerate(data):
        char = bytes([i])
        link.write(char)


try:
    link = serial.Serial(port='COM3', baudrate=115200, timeout=1)
    sleep(3)
    write(data=[0, 0, 0], link=link)
    while True:
        frame_time = time()
        for dimension in dimensions:
            data = capture(dimension)
            write(data, link)
        render_time = time() - frame_time
except KeyboardInterrupt:
    link.close()
    pass
