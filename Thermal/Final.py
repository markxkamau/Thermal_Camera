import serial
from cvzone.SerialModule import SerialObject
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from time import sleep


arduino = serial.Serial("/dev/ttyS0")
arduino2 = SerialObject("/dev/ttyS0")
distance = 1  # declare distance from camera
human_temp_low = 36.0  # declare min human body temperature
human_temp_high = 37.5  # declare max human body temperature
send_alarm = [8, 1]  # turn on alarm
no_alarm = [8, 0]  # turn off alarm
start_camera = [7, 0]  # turn on camera
stop_camera = [7, 1]  # turn off camera


def get_pixel():
    read = 0
    element = 0
    counter = 0
    amg_grid = (8, 8)
    Matrix = [[0 for x in range(amg_grid[0])] for y in range(amg_grid[1])]
    x = 0
    y = 0
    while 1:
        char_var = arduino.readline(1).decode("utf_8")
        if read == 1:
            if char_var == ",":
                Matrix[x][y] = element
                x += 1
                element = 0
                counter = 0
                arduino.read()
            elif ord(char_var) == 13:
                y += 1
                x = 0
                element = 0
                counter = 0
                arduino.read()
            elif char_var == "]":
                read = 0
                x = 0
                y = 0
                break
            elif char_var != ".":
                element += int(char_var)*pow(10, 1-counter)
                counter += 1

        if char_var == "[":
            read = 1
    return Matrix


def response(num):
    if num == 1:
        print(f"Threat Detected {distance} meter away")
        arduino2.sendData(send_alarm)
        sleep(0.3)
        arduino2.sendData(start_camera)
        sleep(0.2)
    elif num == 0:
        arduino2.sendData(no_alarm)
        arduino2.sendData(stop_camera)


pix_res = (8, 8)
xx, yy = (np.linspace(0, pix_res[0], pix_res[0]),
          np.linspace(0, pix_res[1], pix_res[1]))
zz = np.zeros(pix_res)

pix_mult = 10
interp_res = (int(pix_mult*pix_res[0]), int(pix_mult*pix_res[1]))
grid_x, grid_y = (np.linspace(0, pix_res[0], interp_res[0]),
                  np.linspace(0, pix_res[1], interp_res[1]))


def interpole(z_fill):
    f = interpolate.interp2d(xx, yy, z_fill, kind='cubic')
    return f(grid_x, grid_y)


grid_z = interpole(zz)

plt.rcParams.update({'font.size': 16})
fig_dims = (10, 9)
fig, ax = plt.subplots(figsize=fig_dims)
fig.canvas.set_window_title('Thermal Camera View')
im1 = ax.imshow(grid_z, vmin=20, vmax=40, cmap=plt.cm.RdBu_r)
cbar = fig.colorbar(im1, fraction=0.0475, pad=0.03)
cbar.set_label('Temperature [C]', labelpad=10)
fig.canvas.draw()

ax_bgnd = fig.canvas.copy_from_bbox(ax.bbox)
fig.show()


def new_artificial_intelligence(conf_arr):
    human = np.where(
        np.logical_and(conf_arr >= (human_temp_low - distance), conf_arr <= (human_temp_high - distance)))
    if len(conf_arr[human]) != 0:
        return True
    else:
        return False


while True:
    pixels = get_pixel()
    fig.canvas.restore_region(ax_bgnd)
    new_z = interpole(np.reshape(pixels, pix_res))
    im1.set_data(new_z)
    ax.draw_artist(im1)
    fig.canvas.blit(ax.bbox)
    fig.canvas.flush_events()
    if new_artificial_intelligence(new_z):
        response(1)
    else:
        response(0)
