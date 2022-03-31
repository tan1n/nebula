import sys
from time import sleep
import serial
link = serial.Serial(port='COM3', baudrate=115200, timeout=1)
sleep(3)


def write(data, link):
    for i in data:
        char = bytes([i])
        link.write(char)

    # print(link.read())
write(data=[0, 0, 0], link=link)


# link.write(bytes('Ada', 'utf-8'))

# list_data = [255, 0, 0]
# # write(list_data, link)
# print()
