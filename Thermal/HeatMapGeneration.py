
from multiprocessing.connection import wait
import serial
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
import matplotlib.animation as animation

try:
    arduino = serial.Serial("/dev/ttyACM0", 9600)
    print('Connection Estd')
except:
    print('check the port')


def getPixel():
    pixel_list = []
    while True:
        data = []
        row = []

        pdata = arduino.readline().decode("utf")
        if pdata.rstrip() == ']':
            return pixel_list

        row = [i.replace('[', '') for i in pdata.strip().split(',')]

        for i in row:
            try:
                data.append(float(i))
            except:
                print("in for loop exception")
                pass
            if(len(data) == 8):
                pixel_list.append(data)

        # return pixel_list


fig, ax = plt.subplots()


def refreshGraphData(i):
    print("In refresh_graph_data")
    pixel_data = getPixel()
    if len(pixel_data) == 8:
        print('All OK')
        pixel_value = np.array(pixel_data)
        ax.clear()
        ax.imshow(pixel_value, cmap='hot', interpolation='lanczos')
        for i in range(8):
            for j in range(8):
                text = ax.text(
                    j, i, pixel_value[i, j], ha="center", va="center", color="w")
        ax.set_title("Environment Heat Map")
    else:
        print("Pixel not equal to 8")
        ax.clear()


ani = animation.FuncAnimation(fig, refreshGraphData, interval=500)
plt.show()
