import numpy as np
import cv2
from time import sleep, time
import mss
import serial
import mss.tools

start_tine = time()
com_port = '/dev/ttyACM0'
resolution = (1920, 1080)
factor = 10

dimensions = [
    [{"top": factor, "left": factor, "width": resolution[0] -
        factor, "height": 1}, 'top'],  # top
    [{"top": factor+1, "left": resolution[1]-factor, "width": 1,
        "height": resolution[1]-factor}, 'right'],  # right
    [{"top": resolution[1]-factor, "left": factor,
        "width": resolution[0]-factor, "height": 1}, 'bottom'],  # bottom
    [{"top": factor+1, "left": 10, "width": 1,
        "height": resolution[1]-factor}, 'left']  # left
]

led_width = 15
led_height = 8


def capture(args):
    res = (led_width, 1) if args[1] == 'top' or args[1] == 'bottom' else (
        1, led_height)
    with mss.mss() as sct:
        screen = np.array(sct.grab(args[0]))
        img = cv2.resize(screen, res, interpolation=cv2.INTER_NEAREST)
        output = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pixel_data = np.array(output).flatten().tolist()
        if args[1] == 'bottom' or args[1] == 'left':
            return pixel_data.reverse()
        else:
            return pixel_data

def write(data, link):
    for x, i in enumerate(data):
        char = bytes([i])
        link.write(char)
        print(char)

def main():
    link = serial.Serial(port=com_port, baudrate=115200, timeout=1)
    sleep(3)
    write(data=[0, 0, 0], link=link)
    while True:
        for dimension in dimensions:
            data = capture(dimension)
            write(data, link)

# try:
#     main();
# except Exception:
#     # link.close()
#     pass

main()
