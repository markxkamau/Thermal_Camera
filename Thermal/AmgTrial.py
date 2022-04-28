
import numpy as np
import serial
import cv2
import math
from time import sleep
from cvzone.SerialModule import SerialObject

serialport = "/dev/ttyACM0"
scalling = 60  # used to smoothen the image as to more exact figures
distance = 1  # declare distance from camera
send_alarm = [8, 1]  # turn on alarm
no_alarm = [8, 0]  # turn off alarm
start_camera = [7, 0]  # turn on camera
stop_camera = [7, 1]  # turn off camera

width = scalling * 10
height = scalling * 8

img = np.zeros([height, width, 3])
imgGray = np.zeros([height, width, 3])

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
try:
    arduino = serial.Serial(serialport, 9600)
    arduino2 = SerialObject(serialport)
except serial.SerialException:
    print("Cannot open serial port")
    quit()


def response(num):
    if num == 1:
        print(f"Threat Detected {distance} meter away")
        arduino2.sendData(send_alarm)
        sleep(0.4)
        arduino2.sendData(start_camera)
        sleep(0.2)
    elif num == 0:
        arduino2.sendData(no_alarm)
        sleep(0.3)
        arduino2.sendData(stop_camera)


def get_pixel():
    read, element, counter, amg_grid = [0, 0, 0, (8, 8)]
    Matrix = [[0 for x in range(amg_grid[0])] for y in range(amg_grid[1])]
    x, y = [0, 0]
    while 1:
        char_var = arduino.readline(1).decode("utf_8")
        if read == 1:
            if char_var == ",":
                Matrix[x][y] = element
                x += 1
                element, counter = [0, 0]
                arduino.read()
            elif ord(char_var) == 13:
                y += 1
                x = 0
                element, counter = [0, 0]
                arduino.read()
            elif char_var == "]":
                read, x, y = [0, 0, 0]
                break
            elif char_var != ".":
                element += int(char_var)*pow(10, 1-counter)
                counter += 1

        if char_var == "[":
            read = 1
    return Matrix


try:
    print("press Ctrl-C to end")
    while True:
        # read data from serial port
        data = get_pixel()
        # reshape data into matrix
        output = np.reshape(data, (8, 8))

        # scaling
        minValue = math.floor(np.amin(output))
        maxValue = math.ceil(np.amax(output))
        output = output - minValue
        output = output * 255 / (maxValue - minValue)  # Now scaled to 0 - 255

        # resize image
        dim = (width, height)
        output = cv2.resize(output, dim, interpolation=cv2.INTER_CUBIC)

        # apply colormap
        imgGray = output.astype(np.uint8)
        img = cv2.applyColorMap(imgGray, cv2.COLORMAP_OCEAN)

        # process the img gray searching for human using haarcascade
        image_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        colored_img = cv2.cvtColor(imgGray, cv2.COLOR_GRAY2BGR)
        # Reading image and comparing it to the face template
        face = face_cascade.detectMultiScale(image_gray, 1.1, 1)

        # Staying alert to detect human face
        if len(face) != 0:
            print("Faces found:", len(face))
            # drawing rectangles on the spaces registering as faces from the classifier details
            for (x, y, w, h) in face:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 5)
            # set off the alarm alerting the resident
            cv2.imwrite("Threat.jpg", img)
            response(1)
            sleep(1)

        # put min/max text on image
        text = "Min: " + str(minValue) + " C  Max: " + str(maxValue) + " C"
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (20, 50)
        image = cv2.putText(img, text, org, font, 1,
                            (255, 255, 255), 2, cv2.LINE_AA)
        # keep the alarm off unless threat is detected
        response(0)

        cv2.waitKey(50)

        # displaying the live image
        cv2.imshow("Thermal Footage", image)

except KeyboardInterrupt:
    print("Bye bye :)")
    arduino.close()
