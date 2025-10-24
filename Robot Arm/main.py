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

def turn_off(servosList):
    for servo in servosList:
        arm.servoOff(servo)

def get_position(servo):
    print(arm.getPosition(servo))

def set_state(state_name):
    states = {
        "home": [107, 533, 229, 785, 643, 69],
        "ready_to_grab": [286, 489, 142, 738, 357, 490],
        "ready_to_move": [345, 489, 70, 704, 576, 490],
        "grabbed_object": [345, 489, 142, 738, 360, 490]
    }

    if state_name in states:
        print(f"Set to {state_name}")
        for servo in servosList:
            arm.setPosition(servo.servo_id, states[state_name][servo.servo_id - 1])
        return states[state_name]
    else:
        print("Invalid state")

    return None

if __name__ == "__main__":
    #print('Battery voltage in volts:', arm.getBatteryVoltage())
    state_position = set_state("home")
    time.sleep(3)
    state_position = set_state("ready_to_grab")
    time.sleep(3)
    state_position = set_state("grabbed_object")
    time.sleep(3)
    state_position = set_state("ready_to_move")
    time.sleep(3)
    turn_off(servosList)

    




