import sys
from time import sleep
import numpy as np
import serial
# link = serial.Serial(port='COM3', baudrate=115200, timeout=1)
# sleep(3)


# def write(data, link):
#     for i in data:
#         char = bytes([i])
#         link.write(char)

#     # print(link.read())
# write(data=[0, 0, 0], link=link)

arr = [
    [22, 45, 65],
    [255, 90, 81]
]
np_arr = np.array(arr)
pixel = []
for x in arr:
    while len(x) > 0:
        pixel.append(x.pop())

print(pixel[::-1])

# print(np_arr.flatten()[::-1])
# link.write(bytes('Ada', 'utf-8'))

# list_data = [255, 0, 0]
# # write(list_data, link)
# print()
