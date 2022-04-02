import cv2
import serial
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

arduino = serial.Serial("/dev/ttyACM0")
human_temp = 36.0


def get_pixel():
    read = 0
    element = 0
    counter = 0
    amg_grid = (8, 8)
    Matrix = [[0 for x in range(amg_grid[0])] for y in range(amg_grid[1])]
    x = 0
    y = 0
    while 1:
        char = arduino.readline(1).decode("utf")
        if read == 1:
            if char == ",":
                Matrix[x][y] = element
                x += 1
                element = 0
                counter = 0
                arduino.read()
            elif ord(char) == 13:
                y += 1
                x = 0
                element = 0
                counter = 0
                arduino.read()
            elif char == "]":
                read = 0
                x = 0
                y = 0
                break
            elif char != ".":
                element += int(char)*pow(10, 1-counter)
                counter += 1

        if char == "[":
            read = 1
    return Matrix


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
fig.canvas.set_window_title('AMG8833 Image Interpolation')
im1 = ax.imshow(grid_z, vmin=20, vmax=40, cmap=plt.cm.RdBu_r)
cbar = fig.colorbar(im1, fraction=0.0475, pad=0.03)
cbar.set_label('Temperature [C]', labelpad=10)
fig.canvas.draw()

ax_bgnd = fig.canvas.copy_from_bbox(ax.bbox)
fig.show()

pixels_to_read = int(pix_res[0]*pix_mult)


def new_artificial_intelligence(conf_arr):
    human = np.where(
        np.logical_and(conf_arr >= (human_temp - 4.1), conf_arr <= (human_temp+1.0)))
    if len(conf_arr[human]) != 0:
        print("Human Detected")
        return True
    else:
        print("No human detected")
        return False


while True:
    pixels = get_pixel()
    fig.canvas.restore_region(ax_bgnd)
    new_z = interpole(np.reshape(pixels, pix_res))
    cvcheck = np.ndarray((pixels_to_read, pixels_to_read, 3), np.uint8())
    if new_artificial_intelligence(new_z):
        break
    im1.set_data(new_z)
    ax.draw_artist(im1)
    fig.canvas.blit(ax.bbox)
    fig.canvas.flush_events()
