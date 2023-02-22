# Thermal Camera Projects

These projects are aimed at improving security using thermal imaging systems.

## Project 1: MLX90640-Raspberry Pi Thermal Imaging System

### Requirements
- MLX90640 Camera
- Raspberry Pi microprocessor
- Jumper wires
- SD Memory Card
- Mini HDMI cable
- Keyboard and Mouse

### Installation and Setup
1. Install the necessary software and libraries:
   - Raspbian OS
   - Python3
   - OpenCV library
   - MLX90640 Thermal Camera library
2. Connect the MLX90640 Camera to the Raspberry Pi board via jumper wires
3. Connect the Raspberry Pi board to a power source and a display using the Mini HDMI cable
4. Boot up the Raspberry Pi board
5. Clone the project repository and navigate to it
6. Run the Python script using the command `python3 thermal_camera.py`
7. Observe the thermal images displayed on the screen

### Testing
- Run the Python script and observe the thermal images displayed on the screen.
- Test the system by exposing it to different temperatures and observing how the thermal images change.

## Project 2: AMG8833-Arduino Thermal Imaging System

### Requirements 
- AMG88xxx Camera
- Aruino Board
- ESP32-Cam
- Buzzer
- Jumper Cables
- Resistors

### Installation and Setup
1. Install the necessary software and libraries:
   - Arduino IDE
   - ESP32-Cam library
   - Adafruit_AMG88xx library
2. Connect the AMG8833 Camera to the Arduino board via jumper wires
3. Connect the ESP32-Cam to the Arduino board via jumper wires
4. Connect the Buzzer to the Arduino board via jumper wires
5. Connect the Arduino board to a power source
6. Connect the ESP32-Cam to a computer using a USB cable
7. Open the Arduino IDE and select the appropriate board and port
8. Upload the sketch to the Arduino board
9. Disconnect the USB cable from the ESP32-Cam and connect it to a power source
10. Connect to the ESP32-Cam's Wi-Fi network using a mobile device or computer
11. Navigate to the ESP32-Cam's IP address using a web browser
12. Observe the thermal images displayed on the screen

### Contributors
- [Mark Kamau](https://github.com/markxkamau) - author

### Testing
- Test the system by exposing it to different temperatures and observing how the thermal images change.
- Test the buzzer by exposing the system to high temperatures and observing the buzzer sound.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

<!-- # Thermal Camera Projects

## Introduction

This repository contains two projects that utilize thermal imaging to improve security: one using the MLX90640 thermal camera and the Raspberry Pi, and the other using the AMG8833 thermal camera and the Arduino board. 

## Project Overview

The projects are designed to identify objects in the environment based on their temperature, which is picked up by the thermal cameras. The MLX90640-Raspberry Pi project utilizes OpenCV and ML algorithms to identify and classify objects in the camera's field of view. The AMG8833-Arduino project utilizes the ESP32-Cam and a buzzer to alert the user when objects in the field of view exceed a set temperature.

## Installation and Setup

To run these projects, you'll need the following hardware:

- For the MLX90640-Raspberry Pi project:
  - MLX90640 thermal camera
  - Raspberry Pi microprocessor
  - Jumper wires
  - SD Memory Card
  - Mini HDMI cable
  - Keyboard and Mouse

- For the AMG8833-Arduino project:
  - AMG8833 thermal camera
  - Arduino board
  - ESP32-Cam
  - Buzzer
  - Jumper cables
  - Resistors

Additionally, you'll need to have the following software installed:

- Python 3.7 or higher for the MLX90640-Raspberry Pi project
- Arduino IDE for the AMG8833-Arduino project

## Usage

1. Clone the repository to your local machine
2. Follow the circuit diagrams provided in the README for each project to properly wire your components
3. Install any required libraries for the MLX90640-Raspberry Pi project using pip
4. Upload the sketch file to the Arduino board for the AMG8833-Arduino project
5. Run the Python script for the MLX90640-Raspberry Pi project
6. Interact with the project according to its specifications

## Contributors

- [Mark Kamau](https://github.com/markxkamau) - author

## License

This project is licensed under the [MIT License](LICENSE). -->
