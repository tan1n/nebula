import numpy as np
import cv2
from time import sleep, time
import mss
import serial
import mss.tools
from pySerialTransfer import pySerialTransfer as txfer

start_tine = time()
frame = 0


dimensions = [
    [{"top": 0, "left": 0, "width": 1920, "height": 1}, 'top'],  # top
    [{"top": 1, "left": 1919, "width": 1, "height": 1079}, 'right'],  # right
    [{"top": 1079, "left": 0, "width": 1920, "height": 1}, 'bottom'],  # bottom
    [{"top": 1, "left": 0, "width": 1, "height": 1079}, 'left']  # left
]

led_width = 15
led_height = 8


def init_serial():
    link = txfer.SerialTransfer('COM3', 9600)
    link.open()
    return link


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
    for i in data:
        char = bytes(str(i), 'utf-8')
        # char = i
        print(char)
        link.write(char)

# while True:
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         results = [executor.submit(capture, dimension)
#                    for dimension in dimensions]
#       for f in concurrent.futures.as_completed(results):
#         print(f)


try:
    link = serial.Serial(port='COM3', baudrate=115200)
    while True:
        for dimension in dimensions:
            data = capture(dimension)
            write(data, link)
        frame = frame + 1
except KeyboardInterrupt:
    print(frame/(time() - start_tine))
    pass
