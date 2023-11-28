#!/usr/bin/env pybricks-micropython
import random
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile

#------------- INITILIZE ROBOT --------------#
ev3 = EV3Brick()
FL_motor = Motor(Port.A)
FR_motor = Motor(Port.D)
Fan_motor = Motor(Port.B)
ultraSensor = UltrasonicSensor(Port.S3)
touchSensor_L = TouchSensor(Port.S1)
touchSensor_R = TouchSensor(Port.S4)
colorSensor = ColorSensor(Port.S2)
#--------------------------------------------#
global goal_found
global wall_found
global wall_left
global wall_right

# vars
goal_found = False
wall_found = False
wall_left = False
wall_right = False
running = False


# def wallRun():
#     running = True
#     go_forward()
#     while running:
#         print(ultraSensor.distance())
#         while ultraSensor.distance() > 55:
#            # tooFar()
#             if is_wall():
#                 stopRobot()
#                 follow_wall()
#             if colorSensor.color() == Color.BLUE:
#                 running = False
#                 fireFound()
#         while ultraSensor.distance() < 50:
#             # tooClose()
#             if is_wall():
#                 stopRobot()
#                 follow_wall()
#             if colorSensor.color() == Color.YELLOW:
#                 running = False
#                 fireFound()

# def tooClose():
#     FL_motor.run(100)
#     FR_motor.run(150)

# def tooFar():
#     FR_motor.run(100)
#     FL_motor.run(150)

# def timeOut():
#     stopRobot()
#     go_backward()
#     if random.randrange(1, 100) >= 51:
#         turn_right()
#     if random.randrange(1, 100) <= 50:
#         turn_left()

# basic robot functions
def go_forward():
    FL_motor.run(250)
    FR_motor.run(250)
    wait(1000)

def go_backward():
    FL_motor.run(-100)
    FR_motor.run(-100)
    wait(1000)

def turn_left():
    # run_time(speed, time, then=Stop.HOLD, wait=True)
    FR_motor.run_time(250, 1000, then=Stop.HOLD, wait=False)
    FL_motor.run_time(-250, 1000, then=Stop.HOLD, wait=True)
    wait(1000)

def turn_right():
    FL_motor.run_time(250, 1000, then=Stop.HOLD, wait=False)
    FR_motor.run_time(-250, 1000, then=Stop.HOLD, wait=True)
    wait(1000)

def stopRobot():
    FL_motor.brake()
    FR_motor.brake()

def runFan():
    Fan_motor.control.limits(actuation=100)
    Fan_motor.run_time(60000, 5000, then=Stop.HOLD, wait=True)

def extinguishFire():
    Fan_motor.control.limits(actuation=100)
    Fan_motor.run_time(99999999, 5000, then=Stop.HOLD, wait=True)

# wall following functions
def is_wall():
    # using touch sensors to detect wall
    if touchSensor_L.pressed() or touchSensor_R.pressed():
        if touchSensor_L.pressed():
            global wall_left
            wall_left = True
        elif touchSensor_R.pressed():
            global wall_right
            wall_right = True
        return True
    else:
        return False

def is_goal():
    # candle is on yellow paper, so we will check for that color
    if colorSensor.color() == Color.BLUE:
        global goal_found
        goal_found = True
        return True
    else:
        return False

def follow_wall():
    ev3.speaker.say("Following Wall")
    global wall_left
    global wall_right

    # if wall is on left, turn right
    if wall_left == True:
        go_backward()
        turn_right()
        wall_left = False
        go_forward()
    # if wall is on right, turn left
    elif wall_right == True:
        go_backward()
        turn_left()
        wall_right = False
        go_forward()
    # if no wall, go forward
    go_forward()

# wander behavior
def wander():
    # this will ran at the beginning of the program
    # and will run until it finds a wall to follow and
    # the goal is not found
    while not is_wall() and not is_goal():
        go_forward()
        print(colorSensor.color())
    # once a wall is found, follow it
    while is_wall() and not is_goal():
        stopRobot()
        print(colorSensor.color())
        follow_wall()

while not is_goal():
    ev3.speaker.say("Wandering")
    wander()

    # once goal is found, stop
    if is_goal():
        stopRobot()
        print("goal found")
        ev3.speaker.say("Fire")
        extinguishFire()
        wait(300000)

