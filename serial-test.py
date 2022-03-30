import serial
link = serial.Serial(port='COM3', baudrate=115200)


def write(data, link):
    for i in data:
        char = i
        print(char)
        link.write(char)


list_data = [0, 1, 0, 255, 1, 0, 1]
print(bytes(42))
