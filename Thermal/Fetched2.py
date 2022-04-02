import serial
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

ser = serial.Serial('/dev/ttyACM0')
print("Successful Connection")

read = 0
element = 0
counter = 0

amg_grid = (8, 8)
Matrix = [[0 for x in range(amg_grid[0])] for y in range(amg_grid[1])]

x = 0
y = 0

while 1:
    while 1:
        char = ser.readline(1).decode("utf")

        if read == 1:
            if char == ",":
                Matrix[x][y] = element
                x += 1
                element = 0
                counter = 0
                ser.read()
            elif ord(char) == 13:
                y += 1
                x = 0
                element = 0
                counter = 0
                ser.read()
            elif char == "]":
                read = 0
                x = 0
                y = 0
                print("Done")
                break
            elif char != ".":
                element += int(char)*pow(10, 1-counter)
                counter += 1

        if char == "[":
            read = 1
    human_temp = 36.0

    conf_arr = np.array(Matrix)
    human = np.where(
        np.logical_and(conf_arr >= (human_temp - 0.1), conf_arr <= (human_temp+3.0)))
    plt.subplot()
    plt.imshow(conf_arr, vmin=20, vmax=50, interpolation='lanczos')
    plt.colorbar(fraction=0.0475, pad=0.03)
    plt.savefig('confusion_matrix.png')
    plt.show()
