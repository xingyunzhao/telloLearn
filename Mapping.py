import math

import cv2
from djitellopy import tello
import KeyPressModule as kp
from time import sleep
import numpy as np


#################### PARAMETERS ########################
fSpeed = 117 / 10  # Forward Speed in cm/s  (15 cm/s)
aSpeed = 260 / 10  # Angular speed Degrees/s  (50d/s)
interval = 0.25

dInterval = fSpeed * interval
aInterval = aSpeed * interval
########################################################
x, y = 500, 500
a = 0
yaw = 0

kp.init()
my_drone = tello.Tello()
# my_drone.connect()
# print(my_drone.get_battery())

points = [(x, y)]

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    aSpeed = 50
    global x, y, a, yaw
    d = 0

    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180

    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = -aSpeed
        yaw -= aInterval

    elif kp.getKey("d"):
        yv = aSpeed
        yaw += aInterval

    if kp.getKey("e"):
        my_drone.takeoff()
    if kp.getKey("q"):
        my_drone.land()
        sleep(3)

    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return lr, fb, ud, yv, x, y


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 1, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 5, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500)/100}, {(points[-1][1] - 500)/100})m',
                (points[-1][0]+10, points[-1][1]+30), fontFace=cv2.FONT_HERSHEY_PLAIN,
                fontScale=1, color=(255, 0, 255), thickness=1)



while True:
    vals = getKeyboardInput()
    my_drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), dtype=np.uint8)
    if (points[-1][0] != vals[4]) or (points[-1][1] != vals[5]):
        points.append((vals[4], vals[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)



