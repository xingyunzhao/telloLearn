from djitellopy import tello
import KeyPressModule as kp
import time
import cv2


kp.init()
my_drone = tello.Tello()
my_drone.connect()
print(my_drone.get_battery())

global img
my_drone.streamon()


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("d"): yv = speed
    elif kp.getKey("a"): yv = -speed

    if kp.getKey("e"): my_drone.takeoff()
    if kp.getKey("q"): my_drone.land(); time.sleep(3)

    if kp.getKey('z'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.3)

    return lr, fb, ud, yv


# my_drone.takeoff()

while True:
    vals = getKeyboardInput()
    my_drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = my_drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Live Image", img)
    cv2.waitKey(1)


