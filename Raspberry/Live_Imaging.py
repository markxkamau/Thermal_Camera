# -----------------------------------------
# Imports
# =========================================
import time, board, busio
import adafruit_mlx90640
import cv2
import numpy as np
import time
from gpiozero import Buzzer
import math
# =========================================

# -----------------------------------------
# Declarations
# =========================================

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)  # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c)  # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ  # set refresh rate
frame = [0] * 768
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                     'haarcascade_frontalface_alt.xml')
classifier = cv2.CascadeClassifier(cv2.data.haarcascades +
                                   'haarcascade_fullbody.xml')
buzzer = Buzzer(23)
camera = Buzzer(17)
start = {}
stop = {}
# y=(m*x)+c

# =========================================

# -----------------------------------------
# Functions 
# =========================================
def click_event(event, x, y, flags, params):
    # Listening for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        begin = [x,y]
        start[0], start[1] = begin
    # Listening for Right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        end = [x,y]
        stop[0], stop[1] = end

def declare_border():
    while True:
        mlx.getFrame(frame)
        image = np.reshape(frame, (24, 32))
        np.fliplr(image)

        minValue = math.floor(np.amin(image))
        maxValue = math.ceil(np.amax(image))
        image = image - minValue
        image = image * 255 / (maxValue - minValue)  # Now scaled to 0 - 255

        image = cv2.resize(image, (1000, 750), interpolation=cv2.INTER_LANCZOS4)

        imgGray = image.astype(np.uint8)

        img = cv2.applyColorMap(imgGray, cv2.COLORMAP_MAGMA)
        cv2.imshow('Border Declaration', img)
        cv2.setMouseCallback('Border Declaration', click_event)
        if cv2.waitKey(1) == ord('q'):
            break
    

def get_gradient(point1, point2):
    gradient = (point1[1] - point2[1])/(point1[0]-point2[0])
    return gradient

def y_intercept(gradient, point):
    c = point[1] - (gradient * point[0])
    return c

def x_intercept(gradient, y):
    x = (0-y)/gradient
    return x

def value_x(gradient, y, c):
    x = (y-c)/gradient
    return x

def value_y(gradient, x, c):
    y = (gradient * x) + c
    return y

def line_points(gradient, y, x):
    # X = x-intercept
    # Y = y-intercept
    if y < 0:
        x = 0
        while True:
            print("x = ",x,"\ty = ",y)
            if value_y(gradient,x,y) >= 1000:
                value1 = x
                x_value = [(int)(x_intercept(gradient,value1)),0]
                y_value = [0,(int)(value1)]
                print("Xvalue: ",x_value,"Yvalue: ",y_value)

                break
            else:
                x+=1
    if x < 0:
        c = 0
        while True:
            print("c = ",c,"\tx = ",x)
            if value_x(gradient,c,x) >= 750:
                value2 = c
                x_value = [(int)(value2),0]
                y_value = [0,(int)(y_intercept(gradient,start))]
                print("Xvalue: ",x_value,"Yvalue: ",y_value)
                break
            else:
                c+=1
    else:
        x_value = [(int)(x),0]
        y_value = [0,(int)(y)]
    return x_value, y_value
    


def identification():
    return
def location():
    return
# =========================================
# -----------------------------------------
# Main Program
# ========================================= 

declare_border()

cv2.destroyAllWindows()

gradient = get_gradient(start, stop)

point_a, point_b = line_points(gradient,y_intercept(gradient,start),x_intercept(gradient,y_intercept(gradient,start)))

while True:
    
    mlx.getFrame(frame)
    image = np.reshape(frame, (24, 32))
    np.fliplr(image)

    minValue = math.floor(np.amin(image))
    maxValue = math.ceil(np.amax(image))
    image = image - minValue
    image = image * 255 / (maxValue - minValue)  # Now scaled to 0 - 255

    image = cv2.resize(image, (1000, 750), interpolation=cv2.INTER_LANCZOS4)

    imgGray = image.astype(np.uint8)

    img = cv2.applyColorMap(imgGray, cv2.COLORMAP_MAGMA)

    frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face = face_cascade.detectMultiScale(frame_gray)
    body = classifier.detectMultiScale(frame_gray)
    if len(face) != 0:
        print("Faces found:", len(face))
        for (x, y, w, h) in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
        # buzzer.on()
        # camera.off()
    cv2.line(img, point_a, point_b,(255,0,255),5)
    cv2.imshow('custom window', img)
    # buzzer.off()
    # camera.on()

    cv2.waitKey(50)
# =========================================