#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile

# Motor.Control.limits(actuation=75)

#------------- INITILIZE ROBOT --------------#
ev3 = EV3Brick()
FL_motor = Motor(Port.A)
FR_motor = Motor(Port.D)
Fan_motor = Motor(Port.B)
ultraSonic = UltrasonicSensor(Port.S3)
touchSensor_L = TouchSensor(Port.S1)
touchSensor_R = TouchSensor(Port.S4)
colorSensor = ColorSensor(Port.S2)
#--------------------------------------------#

# vars
goal_found = False
wall_found = False
wall_left = False
wall_right = False


# basic robot functions
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

# wall following functions
def is_wall():  
    # using touch sensors to detect wall
    if touchSensor_L.pressed() or touchSensor_R.pressed():
        return True
    else:
        return False

def is_left_wall():
    if touchSensor_L.pressed():
        return True

def is_right_wall():
    if touchSensor_R.pressed():
        return True
    
def is_goal():
    # candle is on yellow paper, so we will check for that color
    if colorSensor.color() == Color.YELLOW:
        return True
    else:
        return False

def follow_wall():
    # if wall is on left, turn right
    if is_wall() and is_left_wall():
        turn_right()
    # if wall is on right, turn left
    elif is_wall() and is_right_wall():
        turn_left()
    # if no wall, go forward
    else:
        go_forward()

# wander behavior
def wander():
    # this will ran at the beginning of the program
    # and will run until it finds a wall to follow and 
    # the goal is not found
    while not is_wall() and not is_goal():
        go_forward()
    # once a wall is found, follow it
    while is_wall() and not is_goal():
        follow_wall()
        # once goal is found, stop
        if is_goal():
            stopRobot()
            runFan()

wander()
