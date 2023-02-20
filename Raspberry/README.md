# Thermal_Camera

This is an IoT project that uses the MLX90640 camera and Raspberry Pi microprocessor to create a thermal imaging system that uses AI to identify thermal images. The system is built using the OpenCV library, and is designed to enhance security in various settings.

## Requirements

To build and run the thermal imaging system, you will need the following components:

- MLX90640 camera
- Raspberry Pi microprocessor
- Jumper wires
- SD memory card
- Mini HDMI cable
- Keyboard and mouse

## Project Circuit

A circuit diagram for the project can be found in the file `circuit_diagram.png`. This diagram shows the correct connections for the various components.

## Installation

To set up the system, follow these steps:

1. Install the Raspbian operating system on the Raspberry Pi.
2. Install OpenCV on the Raspberry Pi.
3. Connect the MLX90640 camera to the Raspberry Pi using the jumper wires.
4. Write and run the Python code to capture and analyze the thermal images.
5. Use the results to enhance security in your desired setting.

### Raspberry Pi Installation

To install Raspbian, follow these steps:

1. Download the latest Raspbian image from the Raspberry Pi website.
2. Write the image to an SD memory card using a tool like Etcher.
3. Insert the SD memory card into the Raspberry Pi and connect it to a display using the mini HDMI cable.
4. Connect the keyboard and mouse to the Raspberry Pi.
5. Power on the Raspberry Pi and follow the on-screen prompts to complete the setup process.

### OpenCV Installation

To install OpenCV on the Raspberry Pi, follow these steps:

1. Update the Raspberry Pi: `sudo apt-get update && sudo apt-get upgrade`
2. Install the required packages: `sudo apt-get install build-essential cmake pkg-config`
3. Install the required image and video I/O libraries: `sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev`
4. Install the GTK development library: `sudo apt-get install libgtk2.0-dev`
5. Install the optimization libraries: `sudo apt-get install libatlas-base-dev gfortran`
6. Download and extract the OpenCV source code: `wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.0.zip && unzip opencv.zip`
7. Create a build directory: `mkdir build && cd build`
8. Configure the build: `cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.0/modules -D BUILD_EXAMPLES=ON ..`
9. Build and install OpenCV: `make -j4 && sudo make install && sudo ldconfig`

### Python Code

The Python code for capturing and analyzing thermal images can be found in the file `thermal_camera.py`. This code uses the OpenCV library to process the data from the MLX90640 camera, and includes machine learning algorithms for identifying thermal images.

To run the code, open it in your preferred Python environment and run it. The results will be displayed on the connected display.

### VSCode

You can also use VSCode to write and run the Python code on the Raspberry Pi. To do this, follow these steps:

1. Install VSCode on your local machine.
2. Install
