#! /usr/bin/python3.7

import os
import sys
import time
import xarm


class Arm:
    def __init__(self, connection_type='USB'):
        self.arm = xarm.Controller(connection_type)

        # Initialize servos
        self.servos = [xarm.Servo(i) for i in range(1, 7)]

        # Define named states
        self.states = {
            "home": [107, 533, 229, 785, 643, 69],
            "ready_to_grab": [286, 489, 142, 738, 357, 490],
            "ready_to_move": [345, 489, 70, 704, 576, 490],
            "grabbed_object": [345, 489, 142, 738, 360, 490],
            "zero": [1000, 500, 500, 500, 500, 500],
        }

    @staticmethod
    def get_python_location():
        """Return the directory where the Python executable is located."""
        return os.path.dirname(sys.executable)

    def turn_off(self):
        """Turn off all servos."""
        for servo in self.servos:
            self.arm.servoOff(servo)
        print("All servos turned off.")

    def get_positions(self):
        """Print current position of all servos."""
        positions = []
        for servo in self.servos:
            pos = self.arm.getPosition(servo)
            positions.append(pos)
            print(f"Servo {servo.servo_id}: {pos}")
        return positions

    def set_state(self, state_name):
        """Set the arm to a predefined state."""
        if state_name not in self.states:
            print(f"Invalid state: {state_name}")
            return None

        print(f"Setting arm to '{state_name}' position...")
        state = self.states[state_name]

        for servo in self.servos:
            self.arm.setPosition(servo.servo_id, state[servo.servo_id - 1])

        return state

    def run_demo_sequence(self):
        """Run a demo sequence of state changes."""
        sequence = ["home", "ready_to_grab", "grabbed_object", "ready_to_move", "zero"]

        for state_name in sequence:
            self.set_state(state_name)
            time.sleep(3)

        self.turn_off()


if __name__ == "__main__":
    arm = Arm()
    arm.run_demo_sequence()