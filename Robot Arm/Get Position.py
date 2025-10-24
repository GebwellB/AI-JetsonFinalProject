import xarm
import time

arm = xarm.Controller('USB')

servosList = []

servo1 = xarm.Servo(1)
servo2 = xarm.Servo(2)
servo3 = xarm.Servo(3)
servo4 = xarm.Servo(4)
servo5 = xarm.Servo(5)
servo6 = xarm.Servo(6)

servosList.append(servo1)
servosList.append(servo2)
servosList.append(servo3)
servosList.append(servo4)
servosList.append(servo5)
servosList.append(servo6)


#for servo in servosList:
#    print(arm.getPosition(servo))

while True:
    if arm.getPosition(servo1) >= 500:
        print("miss")
    else:
        print("yay")
    time.sleep(0.3)
    print(arm.getPosition(servo1))