import cv2 
import numpy as np
import adafruit_mlx90640
import board
import busio
import math

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

# if using higher refresh rates yields a 'too many retries' exception,
# try decreasing this value to work with certain pi/camera combinations
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = [0] * 768
scalling = 60  # used to smoothen the image as to more exact figures
width = scalling * 10
height = scalling * 8
Matrix = [[0 for x in range(24)] for y in range(32)]

face_cascade = cv2.CascadeClassifier( cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

# 1.Collect data from the thermal camera(32*24)
def camera_reading():
    for h in range(24):
        for w in range(32):
            Matrix[w][h] = frame[h * 32 + w]
    return Matrix


while True:
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue

    # 2.Visualise the data using computer vision
    # read data from serial port
    data = camera_reading()
    # reshape data into matrix
    output = np.reshape(data, (32, 24))

        # scaling
    minValue = math.floor(np.amin(output))
    maxValue = math.ceil(np.amax(output))
    output = output - minValue
    output = output * 255 / (maxValue - minValue)  # Now scaled to 0 - 255

    # 3.Interpolation of the live image for smooth images
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

    # 4.Alert response on dectecting humans
    # Staying alert to detect human face
    if len(face) != 0:
        print("Faces found:", len(face))
            # drawing rectangles on the spaces registering as faces from the classifier details
        for (x, y, w, h) in face:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 5)
            # set off the alarm alerting the resident
        cv2.imwrite("Threat.jpg", img)

        # put min/max text on image
    text = "Min: " + str(minValue) + " C  Max: " + str(maxValue) + " C"
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (20, 50)
    image = cv2.putText(img, text, org, font, 1,
                            (255, 255, 255), 2, cv2.LINE_AA)
        # keep the alarm off unless threat is detected

    cv2.waitKey(50)

        # displaying the live image
    cv2.imshow("Thermal Footage", image)
