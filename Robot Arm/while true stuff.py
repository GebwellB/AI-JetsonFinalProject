import xarm
import time

arm = xarm.Controller('USB')

servo1 = xarm.Servo(1)
servo2 = xarm.Servo(2)
servo3 = xarm.Servo(3)
servo4 = xarm.Servo(4)
servo5 = xarm.Servo(5)
servo6 = xarm.Servo(6)

servosList = [servo1, servo2, servo3, servo4, servo5, servo6]

#while True:
#    print('Arm Position:', arm.getPosition(servo1))
#    time.sleep(0.5)

for servo in servosList:
    print(f"Arm Position {servo.servo_id}: ", arm.getPosition(servo))