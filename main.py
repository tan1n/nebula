import numpy as np
import cv2
from time import sleep, time
from mss import mss

width = 1920
height = 1080
led_res = (40, 20)
full = {'left': 0, 'top': 0, 'width': width, 'height': height}
start_tine = time()
frame = 0

try:
    with mss() as sct:
        while True:
            screen = sct.grab(full)
            image = cv2.resize(np.array(screen), led_res,
                               interpolation=cv2.INTER_NEAREST)
            new = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            output = [new[0], new[2], new[:, 2], new[:, 0]]
            frame = frame + 1
except KeyboardInterrupt:
    print(frame/(time() - start_tine))
    pass
