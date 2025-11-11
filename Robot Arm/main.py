import xarm
import time
import cv2
import os

camera = cv2.VideoCapture(0)

output_folder = "Robot Arm/Arm Training"
os.makedirs(output_folder, exist_ok=True)

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

def get_positions(servo):
    return(f"{arm.getPosition(servo)}")

def take_photo():
    pass

def set_state(state_name):
    states = {
        "home": [107, 533, 167, 905, 875, 497],
        "ready_to_grab": [90, 490, 143, 738, 357, 490],
        "ready_to_move": [0, 490, 70, 704, 576, 490],
        "grabbed_object": [1000, 489, 143, 738, 360, 490],
        "zero": [1000, 500, 500, 500, 500, 500]
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
    #time.sleep(3)
    #state_position = set_state("ready_to_grab")
    #time.sleep(3)
    #state_position = set_state("grabbed_object")
    #time.sleep(3)
    #state_position = set_state("ready_to_move")
    time.sleep(1)
    #state_position = set_state("zero")
    #time.sleep(3)
    turn_off(servosList)
    return_value, image = camera.read()
    #output_filename = os.path.join(output_folder, f'arm_pos_{get_positions(servo1)}_{get_positions(servo2)}_{get_positions(servo3)}_{get_positions(servo4)}_{get_positions(servo5)}_{get_positions(servo6)}.png')
    output_filename = os.path.join(output_folder, "arm_pos_ .png")
    cv2.imwrite(output_filename, image)
    print("PHOTO TAKEN, MOVE IN NOW")
    old_name = "arm_pos_ .png"
    countdown = 10

    for i in range(10):
        print(countdown)
        countdown -= 1
        time.sleep(1)

    print(f"arm_pos_{get_positions(servo1)}_{get_positions(servo2)}_{get_positions(servo3)}_{get_positions(servo4)}_{get_positions(servo5)}_{get_positions(servo6)}")

    new_name = f"{get_positions(servo1)}_{get_positions(servo2)}_{get_positions(servo3)}_{get_positions(servo4)}_{get_positions(servo5)}_{get_positions(servo6)}.png"

    old_path = os.path.join(output_folder, old_name)
    new_path = os.path.join(output_folder, new_name)

    os.rename(old_path, new_path)

    print(f"✅ Renamed:\n{old_path}\n→ {new_path}")

    state_position = set_state("ready_to_move")

    time.sleep(3)

    turn_off(servosList)

    print("DONE!")
