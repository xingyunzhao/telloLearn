from djitellopy import tello
from time import sleep

my_drone = tello.Tello()
my_drone.connect()
print(my_drone.get_battery())

my_drone.takeoff()
sleep(3)
my_drone.send_rc_control(0, 30, 10, 0)
sleep(1)
my_drone.send_rc_control(0, 0, 0, 0)
sleep(3)
my_drone.land()

