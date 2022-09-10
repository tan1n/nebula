from tkinter import *
from tkinter.colorchooser import askcolor
from numpy import pad

window = Tk()
window.title('Nebula ambilight')
statusLabel = Label(window, text='Status :').grid(
    row=0, column=0, padx=10, pady=10)
statusInput = Entry(window, width=20, state='disabled').grid(row=0, column=1)
portLabel = Label(window, text='Device port :').grid(row=0, column=2, padx=10)
COMOPTIONS = [
    "COM1",
    "COM3",
    "COM4"
]
comVariable = StringVar(window).set(COMOPTIONS[0])
portInput = OptionMenu(window, comVariable, *COMOPTIONS).grid(row=0, column=3)
resolutionLabel = Label(window, text='Resolution :').grid(
    row=1, column=0, padx=10)
displayLabel = Label(window, text="Display size :").grid(
    row=2, column=0, padx=10, pady=10)
displayInput = Entry(window).grid(row=2, column=1)
ledWidthLabel = Label(window, text='LED width:').grid(row=2, column=2)
ledWidthInput = Entry(window, width=2).grid(row=2, column=3)
ledHeightLabel = Label(window, text='LED height:').grid(row=2, column=4)
ledHeightInput = Entry(window, width=2).grid(row=2, column=5, padx=10)
ledDefaultLabel = Button(window, text='Default').grid(row=2, column=6)
lightingModeLabel = Label(window, text="Mode").grid(row=3, column=0, pady=10)
modeVer = IntVar()
ambilightRadio = Radiobutton(
    window, text="Ambilight", variable=modeVer, value=1).grid(row=3, column=1)
staticRadio = Radiobutton(
    window, text="Static", variable=modeVer, value=2).grid(row=3, column=2)
staticColorButton = Button(window, text='Select a color').grid(row=3, column=3)
startBtn = Button(window, text='Start', width=10, height=3).grid(padx=10)
window.geometry("640x320")
window.resizable(0, 0)
window.mainloop()
