
This project is a two axis pointing system to support various astronomy projects.

The system components are a BNO055 9 axis IMU and a pointer assembly of two stepper
motors on an altitude/azimuth (pan and tilt) mount.  The motors are driven by a kitronics Pico Robotics Board. 
Data is collected and transmitted by RaspberryPi PicoWs making the system both server- and wire-less.


## Data choice 
The BNO055 outputs several types of direct measurements (Mag, Gyro, Acc, etc) and two sets of derived information, Euler Angles and Quaternions.  A quick review of literature suggests that Euler Angles can be problematic, and it is best to use quaternions in any data manipulations only converting to Euler angels in the last steps. 
This does not see to hold for the BNO055.  Initially data was erratic prompting a strategy of averaging the output.  The output is received in multi layer dictionary structures, so a utility was written to flatten the dictionary and average them (utils/flatten_dict.py).  Another utility was written to convert quaternions to Euler angels (utils/quaternion.py). 

The Euler angles output it from the sensor seem to be quite stable and correspond well with the orientation of the chip.  the decision was made to use the output from the chip directly ignoring the quaternions for now. It is worth investigating the processing done on the microprocessor of the BNO055 there appears to be some smoothing in the output data evidenced by its stability. 

When the Euler angles are sent Stellarium they must first be inverted by multiplying by -1 and then converting into radians 

## BNO055 Board layout and orientation:
         +----------+
         |         *| RST   PITCH  ROLL  HEADING
     ADR |*        *| SCL
     INT |*        *| SDA     ^            /->
     PS1 |*        *| GND     |            |
     PS0 |*        *| 3VO     Y    Z-->    \-X
         |         *| VIN
         +----------+





Circuitpython does not yet support PicoW




# Micropython for the PICOw
[https://micropython.org/download/rp2-pico-w/]()

# see this for getting on line
<https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf>

# pico-nuke
use this to reset the PICO and prepare for a fresh install of Micropython
<https://github.com/polhenarejos/pico-nuke>

# PICO Robotics Board 
https://github.com/KitronikLtd/Kitronik-Pico-Robotics-Board-MicroPython

IDE can be either Thonny or Pycharm
if Pycharm use the Micropython plug in
ampy may need to be rolled back, this scan be done in the project Settings 

When using Pycharm close all other instances of the REPL before Flashing the device.   

# Set up 
in Pycharm using a conda virtual environment with Python 3.10 (the defaults), the dependency Adafruit-ampy does not install automatically 

use: 
'''
pip install adafruit-ampy
'''

# Stellarium Set up

ref https://stellarium.org/doc/head/remoteControlApi.html

Launch Stellarium Application 

Go to 	
1. Configuration Menu (F2)
2. Select the Plug-ins icon (top of dialogue box)
3. Select Remote Control plug-in (left of dialogue box)
4. Check box - launch at startup

Restart Stellarium Application to load plug-in

Return to the Remote Control plug-in

1. Click the Configure button
2. Check box: the Server enabled box 
   1. Returns: listening on 127.0.1.1
3. Confirm: Port number: 8096
4. Check box: Enable automatically at start up 
5. Save settings
