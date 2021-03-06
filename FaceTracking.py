import time

import cv2
import numpy as np
from djitellopy import tello

my_drone = tello.Tello()
my_drone.connect()
print(my_drone.get_battery())

my_drone.streamon()
my_drone.takeoff()
my_drone.send_rc_control(0, 0, 25, 0)
time.sleep(3.0)


w, h = 360, 240
fbRange = [6200, 6800]  # forward and backward range of face area
pid = [0.4, 0.4, 0]
pError = 0


def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []  # face center list
    myFaceListArea = []  # face area list

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cx = x + w//2
        cy = y + w//2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(info, w, pid, pError):

    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w//2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if (fbRange[0] <= area <= fbRange[1]):
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif 0 < area < fbRange[0]:
        fb = 20
    else:  # area <= 0 error or undetected scenario
        fb = 0

    if x == 0:
        speed = 0
        error = 0

    # print(speed, fb)
    my_drone.send_rc_control(0, fb, 0, speed)

    return error


# cap = cv2.VideoCapture(0)
out = cv2.VideoWriter("Resources/Video/record.avi", cv2.VideoWriter_fourcc(*'XVID'), 25, (w, h))


while True:
    # _, img = cap.read()
    img = my_drone.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError)
    # print("Area", info[1], "Center", info[0])
    out.write(img)
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        my_drone.land()
        break

out.release()
cv2.destroyAllWindows()
