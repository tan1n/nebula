from cv2 import INTER_AREA
import numpy as np
import cv2
from time import sleep, time
import mss
import mss.tools
import serial.tools.list_ports

aspect_ratio = {'4:3': (4, 3), '16:9': (16, 9), '21:9': (21, 9)}
resolution = (1920, 817)
offset = 150
frame = 0
total_fps = 0
total_frame = 0

dimensions = [
    [
        {
            "top": offset,
            "left": 0,
            "width": offset,
            "height": resolution[1]-(offset*2)
        },
        'left'
    ],
    [
        {
            "top": resolution[1]-817,
            "left": 0,
            "width": resolution[0],
            "height": offset
        },
        'top'
    ],
    [
        {
            "top": offset,
            "left": resolution[0]-offset,
            "width": offset,
            "height": resolution[1]-(offset*2)
        },
        'right'
    ],
    # [
    #     {
    #         "top": resolution[1]-offset,
    #         "left": 0,
    #         "width": resolution[0],
    #         "height": offset
    #     },
    #     'bottom'
    # ],
]

led_width = 12
led_height = 7


def discover_device():
    comlist = serial.tools.list_ports.comports()
    for element in comlist:
        connection = serial.Serial(
            port=element.device, baudrate=115200, timeout=1)
        sleep(1)
        read = connection.read()
        if read == b'F':
            return connection
        if read == b'A' and connection.writable():
            start_time = time() + 30;
            # Implement timeout
            while(connection.read() != b'C'):
                if start_time < time():
                    connection = False
                    break 
                connection.write('Nebula'.encode('utf-8'))
            return connection
        else:
            connection.close()
    return False


link = discover_device()

def capture(args):
    res = (led_width, 1) if args[1] == 'top' or args[1] == 'bottom' else (
        1, led_height)
    with mss.mss() as sct:
        screen = np.array(sct.grab(args[0]))
        img = cv2.resize(screen, res, interpolation=INTER_AREA)
        output = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        output = cv2.GaussianBlur(output, (5, 5), 0)
        pixel_data = np.array(output)
        if args[1] == 'bottom' or args[1] == 'left':
            return reverse_pixels(pixel_data.tolist(), args[1])
        else:
            return pixel_data.flatten().tolist()


def reverse_pixels(pixel_arr, type):
    data = pixel_arr[0] if type == 'bottom' else pixel_arr
    pixel = []
    for x in data:
        while len(x) > 0:
            pixel.append(x.pop())
    if type == 'bottom':
        return pixel[::-1]
    else:
        return np.array(pixel).flatten().tolist()


def write(data, checksum=True):
    if checksum:
        link.write('Frames'.encode('utf-8'))
    for i in data:
        char = bytes([i])
        link.write(char)


def main():
    global ambilight
    global frame
    global total_frame
    global total_fps
    while ambilight:
        frame = 0
        start_time = time()
        i = 0
        queue = []
        for dimension in dimensions:
            data = capture(dimension)
            queue.append(data)
            i += 1
        write(np.hstack(queue))
        frame += 1
        total_fps += frame / (time() - start_time)
        total_frame += 1


ambilight = True

try:
    main()
except KeyboardInterrupt:
    empty = np.empty((led_height*2)+(led_width*2), dtype=int)
    empty.fill(255)
    write(empty, False)
    link.write(b'D')
    link.close()
    print(total_fps/total_frame)
pass

## music sync 
## static
## 
## navbar #edffed  sidebar #eeffec