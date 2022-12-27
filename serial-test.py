import sys
from time import sleep
import numpy as np
import serial
link = serial.Serial(port='COM4', baudrate=115200, timeout=1)
# link.write('Nebula'.encode('utf-8'))
# print(np_arr.flatten()[::-1])
link.write(str(33).encode('utf-8'))
link.close()

# list_data = [255, 0, 0]
# # write(list_data, link)
# print()
