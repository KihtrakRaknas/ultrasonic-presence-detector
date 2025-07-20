# Ultrasonic Presence Detector

This code was written in MicroPython to run on a Raspberry Pi Pico W.
The goal is to utilize a HC-SR04 ultrasonic sensor to detect presence.
When presence is detected, the provided webhook will be called.

## Set Up

Create a `config.py` folder using `config.py.template` as a reference.

The recommended way to upload MicroPython code to a Raspberry Pi Pico W is using
Thonny. You can upload the python files in this repo through the tool.
