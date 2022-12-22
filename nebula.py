import tkinter as tk
from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image
from math import ceil
import json
from cv2 import INTER_AREA
import numpy as np
import cv2
from time import sleep, time
import mss
import mss.tools
import serial.tools.list_ports
import pystray
from pystray import MenuItem as item
from tkinter import messagebox
import customtkinter
from threading import *


run_device = False

# config file
config_file = open('config.json')
configs = json.load(config_file)

# write to config


def write_config():
    with open('config.json', 'w') as file:
        json.dump(configs, file)

# ui functions


def get_state():
    global run_device
    if run_device:
        return tk.DISABLED
    else:
        return tk.NORMAL


def modeClicked(value):
    mode.set(value)
    if value == 'static':
        mainToggleButton.configure(text='Set color')
    else:
        mainToggleButton.configure(text='Start')
    configs['mode'] = value
    write_config()


def change_color():
    colors = askcolor(title="Pick A Static Color")
    if colors[0]:
        configs['static_color'] = list(colors[0])
        colorAskButton.configure(fg_color=get_color_hex())
        write_config()


def ambModeClicked(value):
    AmbMode.set(value)
    configs['ambient_mode'] = value
    write_config()


def change_display(value):
    configs['display_size'] = SizeOption[value]
    write_config()

# Light code


def discover_device():
    comlist = serial.tools.list_ports.comports()
    for element in comlist:
        connection = serial.Serial(
            port=element.device, baudrate=115200, timeout=1)
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
    return ceil(((pos)*0.0254)*30) - 1


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
        if device.isOpen():
            device.write('Frames'.encode('utf-8'))
    for i in data:
        char = bytes([i])
        if device.isOpen():
            device.write(char)


def disconnect():
    global device
    global run_device
    run_device = False
    change_states()
    deviceStatusLabel.configure(
        text='Device disconnected', text_color='#FF2D00')
    if configs['mode'] == 'static':
        mainToggleButton.configure(text='Set color')
    else:
        mainToggleButton.configure(text='Start')
    mainToggleButton.configure(command=begin, fg_color='black')
    device.write('D'.encode('utf-8'))
    device.close()


def set_config():
    global device
    leds = str(led_width+led_height*2).encode('utf-8')
    device.write(leds)


def start_device():
    global dimensions
    global run_device
    if configs['mode'] == 'static':
        total_leds = led_width+led_height*2
        queue = []
        for x in range(0, total_leds):
            for y in configs['static_color']:
                queue.append(y)
        write(queue)
        disconnect()
    else:
        while run_device:
            queue = []
            for dimension in dimensions:
                data = capture(dimension)
                queue.append(data)
            write(np.hstack(queue))


def begin():
    global run_device
    global device
    device = discover_device()
    if device:
        run_device = True
        deviceStatusLabel.configure(
            text='Device connected', text_color='#00FF2E')
        set_config()
        change_states()
        mainToggleButton.configure(
            text='Disconnect', command=disconnect, fg_color='#FF0000')
        t = Thread(target=start_device)
        t.start()
    else:
        run_device = False
        deviceStatusLabel.configure(text='Device not found')
        messagebox.showwarning(
            "Warning", "No device found. Please connect again and please try again")


resolution = (1920, 817)
offset = 10 if configs['ambient_mode'] == 'gaming' else 250
dimensions = [
    [
        {
            "top": offset,
            "left": 0,
            "width": offset,
            "height": resolution[1]-(offset)
        },
        'left'
    ],
    [
        {
            "top": 0,
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
            "height": resolution[1]-(offset)
        },
        'right'
    ],
]
led_width = led_count(ceil(configs['display_size']*.875))
led_height = led_count(ceil(configs['display_size']*.49))

# UI CODE

root = customtkinter.CTk()
root.resizable(width=False, height=False)
root.title("Nebula Ambilights")
root.eval('tk::PlaceWindow . center')


# On Window quit
def quit_window(icon, item):
    global run_device
    run_device = False
    icon.stop()
    root.destroy()

# Define a function to show the window again


def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

# Hide the window and show on the system taskbar


def hide_window():
    global run_device
    root.withdraw()
    image = Image.open("favicon.ico")
    menu = (item('Quit', quit_window), item(
        'Show', show_window))
    if run_device:
        menu = list(menu)
        menu.insert(2, item('Disconnect', disconnect))
        menu = tuple(menu)
    icon = pystray.Icon("Nebula", image, "Nebula Ambilight", menu)
    icon.run()


def get_color_hex():
    return '#%02x%02x%02x' % tuple(configs['static_color'])


def change_states():
    widgets = [displaySizeMenu, ambientModeRadioButton, staticModeRadioButton,
               movieModeRadioButton, gamingModeRadioButton, colorAskButton]
    for x in widgets:
        x.configure(state=get_state())


# states
displaySize = StringVar()
displaySize.set(
    "Display Size" if configs['display_size'] == '' else configs['display_size'])

mode = StringVar()
mode.set("ambient" if configs['mode'] == '' else configs['mode'])

# Status
customtkinter.CTkLabel(root, text="Status :").grid(
    row=0, column=0, sticky='w', padx=10, pady=3)
deviceStatusLabel = customtkinter.CTkLabel(
    root, text='Not Connected', text_color='#FF2D00')
deviceStatusLabel.grid(row=0, column=1, sticky="w")
# Display size
SizeOption = {
    "17 Inch": 17,
    "19 Inch": 19,
    "21 Inch": 21,
    "22 Inch": 22,
    "24 Inch": 24,
    "27 Inch": 27,
    "29 Inch": 29,
    "32 Inch": 32,
    "28 Inch": 28,
    "43 Inch": 43,
    "49 Inch": 49,
}
customtkinter.CTkLabel(root, text="Display Size :").grid(
    row=1, column=0, sticky="nw", padx=10,)
displaySizeMenu = customtkinter.CTkOptionMenu(root, variable=displaySize, values=list(SizeOption.keys()),
                                              command=change_display)
displaySizeMenu.grid(row=1, column=1)
customtkinter.CTkLabel(root, text="Lighting Mode :").grid(
    row=4, column=0, sticky="nw", padx=10, pady=5)
ambientModeRadioButton = customtkinter.CTkRadioButton(root, text="Ambient", variable=mode, value="ambient", command=lambda: modeClicked(
    mode.get()))
ambientModeRadioButton.grid(row=5, column=0, sticky="nw", padx=15)
staticModeRadioButton = customtkinter.CTkRadioButton(root, text="Static", variable=mode, value="static", command=lambda: modeClicked(
    mode.get()))
staticModeRadioButton.grid(row=5, column=1, sticky="nw")
colorAskButton = customtkinter.CTkButton(
    root, text='Change Color', command=change_color, fg_color=get_color_hex(), width=60)
colorAskButton.grid(row=5, column=2, sticky='nw')
customtkinter.CTkLabel(root, text="Mode:").grid(
    row=6, column=0, padx=10, sticky="nw", pady=5)
# Ambient mode
AmbMode = StringVar()
AmbMode.set(configs['ambient_mode'])
movieModeRadioButton = customtkinter.CTkRadioButton(root, text="Movie Mode", variable=AmbMode, value="movie", command=lambda: ambModeClicked(
    AmbMode.get()))
movieModeRadioButton.grid(row=7, column=0, sticky="nw", padx=15)
gamingModeRadioButton = customtkinter.CTkRadioButton(root, text="Gaming Mode", variable=AmbMode, value="gaming", command=lambda: ambModeClicked(
    AmbMode.get()))
gamingModeRadioButton.grid(row=7, column=1, sticky="nw")
# Run on startup
StartUpRun = IntVar()
customtkinter.CTkCheckBox(root, text='Start up',
                          variable=StartUpRun, onvalue=1, offvalue=0,).grid(row=7, column=2, sticky="nw")
mainToggleButton = customtkinter.CTkButton(
    root, text="Start", command=begin, fg_color='black')
mainToggleButton.grid(row=8, column=0, columnspan=4, padx=30, pady=30)
root.protocol('WM_DELETE_WINDOW', hide_window)
root.iconbitmap('favicon.ico')
root.mainloop()
