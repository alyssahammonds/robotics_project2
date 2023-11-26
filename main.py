#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile

# Motor.Control.limits(actuation=75)

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# direction = 'N'  # current direction
#--------------------------------------------#

#------------- INITILIZE ROBOT --------------#
ev3 = EV3Brick()
FL_motor = Motor(Port.A)
FR_motor = Motor(Port.D)
Fan_motor = Motor(Port.B)
ultraSonic = UltrasonicSensor(Port.S3)
touchSensor_L = TouchSensor(Port.S1)
touchSensor_R = TouchSensor(Port.S4)
#--------------------------------------------#

#------------- FUNCTIONS --------------------#
def go_forward():
    FL_motor.run(250)
    FR_motor.run(250)
    wait(1000)

def go_backward():
    FL_motor.run(-360)
    FR_motor.run(-360)
    wait(1000)

def turn_left():
    # run_time(speed, time, then=Stop.HOLD, wait=True)
    FR_motor.run_time(500, 1000, then=Stop.HOLD, wait=False)
    FL_motor.run_time(-500, 1000, then=Stop.HOLD, wait=True)
    wait(1000)

def turn_right():
    FL_motor.run_time(500, 1000, then=Stop.HOLD, wait=False)
    FR_motor.run_time(-500, 1000, then=Stop.HOLD, wait=True)
    wait(1000)

def stopRobot():
    FL_motor.brake()
    FR_motor.brake()

def runFan():
    Fan_motor.run_time(60000, 5000, then=Stop.HOLD, wait=True)

def leftTouch():
    touchSensor_L.wait_for_pressed(None, 10)

def rightTouch():
    touchSensor_R.wait_for_pressed(None, 10)

#------------- PROGRAM --------------------#

while not touchSensor_L.pressed() or touchSensor_R.pressed():
    go_forward()
    if touchSensor_L.pressed() or touchSensor_R.pressed():
        ev3.speaker.beep()
        stopRobot()
    wait(1000)

ev3.speaker.beep()
