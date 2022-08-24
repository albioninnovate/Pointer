

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
