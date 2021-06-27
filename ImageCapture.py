from djitellopy import tello
import cv2

my_drone = tello.Tello()
my_drone.connect()
print(my_drone.get_battery())

my_drone.streamon()

while True:
    img = my_drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Live Image", img)
    cv2.waitKey(1)



