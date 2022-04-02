import serial

arduino = serial.Serial("/dev/ttyACM0")


while True:
    pdata = arduino.readline().decode('utf')

    # arduino.write(myString.encode())

    print(pdata.rstrip())
