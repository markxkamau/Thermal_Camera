import math
import time
import numpy as np
import board
import busio
import adafruit_mlx90640
import cv2
from gpiozero import Buzzer
# import RPi.GPIO as gpio

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = [0] * 768

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                     'haarcascade_frontalface_alt.xml')
classifier = cv2.CascadeClassifier(cv2.data.haarcascades +
                                   'haarcascade_fullbody.xml')

buzzer = Buzzer(23)

camera = Buzzer(17)

while True:
    mlx.getFrame(frame)
    image = np.reshape(frame, (24, 32))
    np.fliplr(image)

    minValue = math.floor(np.amin(image))
    maxValue = math.ceil(np.amax(image))
    image = image - minValue
    image = image * 255 / (maxValue - minValue)  # Now scaled to 0 - 255

    # image = cv2.resize(image, (1000, 750), interpolation=cv2.INTER_LINEAR_EXACT)
    # Second Option for more accuracy
    image = cv2.resize(image, (1000, 750), interpolation=cv2.INTER_LANCZOS4)

    imgGray = image.astype(np.uint8)

    img = cv2.applyColorMap(imgGray, cv2.COLORMAP_MAGMA)

    # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face = face_cascade.detectMultiScale(frame_gray)
    body = classifier.detectMultiScale(frame_gray)
    if len(face) != 0:
        print("Faces found:", len(face))

        for (x, y, w, h) in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
        buzzer.on()
        camera.off()
    # cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('custom window', img)
    buzzer.off()
    camera.on()
    # cv2.resizeWindow('custom window', 1000, 1000)

    cv2.waitKey(50)
    # cv2.imshow("Thermal Footage", image)
