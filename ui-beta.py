from cProfile import run
from  tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image
from math import ceil
import json
from cv2 import INTER_AREA
import numpy as np
import cv2
from time import sleep, time
import mss
import mss.tools
import serial.tools.list_ports

run_device = False;
device_found = False;

# config file
config_file = open('config.json');
configs = json.load(config_file);

# write to config
def write_config():
    with open('config.json','w') as file:
        json.dump(configs,file)

# ui functions
def modeClicked(value):
    mode.set(value)
    configs['mode'] = value
    write_config() 

def change_color():
    colors = askcolor(title="Pick A Static Color")
    write_config() 

def ambModeClicked(value):
    AmbMode.set(value)
    configs['ambient_mode'] = value
    write_config()

def change_display(value):
    configs['display_size'] = SizeOption[value];
    write_config()

# Light code
def discover_device():
    comlist = serial.tools.list_ports.comports()
    for element in comlist:
        connection = serial.Serial(port=element.device, baudrate=115200, timeout=1)
        sleep(1)
        read = connection.read()
        if read == b'A' and connection.writable():
            start_time = time() + 30
            while(connection.read() != b'C'):
                if start_time < time():
                    connection = False
                    break 
                connection.write('Nebula'.encode('utf-8'))
            return connection
        else:
            connection.close()
    return False


def led_count(pos):
    return ceil((((pos/2)/12)/3.33)*30) - 1

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
    global device
    if checksum:
        device.write('Frames'.encode('utf-8'))
    for i in data:
        char = bytes([i])
        device.write(char)

def start_device():
    global dimensions
    global run_device
    queue = []
    for dimension in dimensions:
        data = capture(dimension)
        queue.append(data)
    write(np.hstack(queue))
    if run_device:
        root.after(20,start_device)

def begin():
    global run_device;
    global device;
    run_device = True
    device = discover_device()
    if device :
        status.set('Device connected')
        start_device()
    else:
        status.set('Device not found')

resolution = (1920, 817)
offset = 250
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
]
led_width = led_count(ceil((configs['display_size']*.875)*2))
led_height = led_count(ceil((configs['display_size']*.49)*2))

# UI CODE
root= Tk()
root.title("Nebula Ambilights")
root.eval('tk::PlaceWindow . center')

# states
status = StringVar()
status.set("Not connected")

displaySize = StringVar()
displaySize.set("Display Size" if configs['display_size'] == '' else configs['display_size'])

mode = StringVar()
mode.set("ambient" if configs['mode'] == '' else configs['mode'])

# Status
Label(root, text="Status :",font=('Aerial 11 bold')).grid(row=0, column=0, sticky="nw", padx=10, pady=10)
Label(root, text=status.get(),font=('Aerial 10')).grid(row=0, column=1)
# Display size
SizeOption = {
"17 Inch" : 17,
"19 Inch" : 19,
"21 Inch" : 21,
"22 Inch" : 22,
"24 Inch" : 24,
"27 Inch" : 27,
"29 Inch" : 29,
"32 Inch" : 32,
"28 Inch" : 28,
"43 Inch" : 43,
"49 Inch" : 49,
}
Label(root, text="Display Size :",font=('Aerial 11 bold')).grid(row=1, column=0, sticky="nw",padx=10,)
OptionMenu(root, displaySize, *SizeOption,command=change_display).grid(row=1, column=1)
# Logo
img = ImageTk.PhotoImage(Image.open("logo1.png").resize((100, 50), ))
Label(root, image = img).place(x=320, y=20)
# Frame
frame=Frame(root,)
Label(frame, text="Lighting Mode :",font=('Aerial 11 bold')).grid(row=4, column=0, sticky="nw",padx=10, pady=5)
Radiobutton(frame, text="Ambient", variable=mode, value="ambient", command=lambda: modeClicked(mode.get()),font=('Aerial 10')).grid(row=5, column=0,sticky="nw",padx=15)
Radiobutton(frame, text="Music Sync", variable=mode, value="music", command=lambda: modeClicked(mode.get()),font=('Aerial 10')).grid(row=5, column=1,sticky="nw")
Radiobutton(frame, text="Static", variable=mode, value="static", command=lambda: modeClicked(mode.get()),font=('Aerial 10')).grid(row=5, column=2,sticky="nw")
ttk.Button(frame, text='Select a Color', command=change_color).grid(row=5, column=3, padx=30)
frame.grid(pady=20, columnspan=5)
Label(root, text="Ambient Mode :",font=('Aerial 11 bold')).grid(row=6, column=0, padx=10,sticky="nw", pady=5)
# Ambient mode
AmbMode = StringVar()
AmbMode.set("movie")
Radiobutton(root, text="Movie Mode", variable=AmbMode, value="movie", command=lambda: ambModeClicked(AmbMode.get()),font=('Aerial 10')).grid(row=7, column=0,sticky="nw",padx=15)
Radiobutton(root, text="Gaming Mode", variable=AmbMode, value="gaming", command=lambda: ambModeClicked(AmbMode.get()),font=('Aerial 10')).grid(row=7, column=1,sticky="nw")
# Run on startup
StartUpRun = IntVar()
Checkbutton(root, text='Run on start up',variable=StartUpRun, onvalue=1, offvalue=0,font=('Aerial 11')).grid(row=7, column=3)
Button(root, text="Start",bg='green',fg='white',bd=3,font=('Aerial 11'),command=begin).grid(row=8, column=0, columnspan=4, ipadx=30,pady=30)
root.mainloop()