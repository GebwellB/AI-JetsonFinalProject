import torch
import cv2
from PIL import Image
from torchvision import transforms
from ultralytics import YOLO
import time
import xarm

arm = xarm.Controller('USB')

servo1 = xarm.Servo(1)
servo2 = xarm.Servo(2)
servo3 = xarm.Servo(3)
servo4 = xarm.Servo(4)
servo5 = xarm.Servo(5)
servo6 = xarm.Servo(6)

servosList = [servo1, servo2, servo3, servo4, servo5, servo6]

# YOLO model
yolo_model = YOLO(r'Robot Arm/number_4_detector.pt')  

# Robot servo model
class RobotModel(torch.nn.Module):
    def __init__(self):
        super(RobotModel, self).__init__()
        self.conv = torch.nn.Sequential(
            torch.nn.Conv2d(3, 16, 3, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(16, 32, 3, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(32, 64, 3, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.AdaptiveAvgPool2d((1,1))
        )
        self.fc = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(64, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 6)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

servo_model = RobotModel()
servo_model.load_state_dict(torch.load(r"Robot Arm/best_robot_arm_model.pth", map_location='cpu'))
servo_model.eval()

# Transform for images
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

CONF_THRESHOLD = 0.8  # confidence threshold for YOLO

cap = cv2.VideoCapture(0)

def set_state(state_name):
    states = {
        "home": [107, 533, 167, 905, 875, 497],
        "ready_to_grab": [90, 490, 143, 738, 357, 490],
        "ready_to_move": [300, 490, 70, 704, 576, 490],
        "grabbed_object": [400, 489, 143, 738, 360, 490],
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

set_state("home")
time.sleep(2)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO detection
        results = yolo_model(frame)

        for box in results[0].boxes:
            conf = float(box.conf[0])
            cls = int(box.cls[0])

            if cls == 0 and conf >= CONF_THRESHOLD:
                # Crop detected object
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                crop = frame[y1:y2, x1:x2]
                crop_pil = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
                input_tensor = transform(crop_pil).unsqueeze(0)

                # Predict servo positions
                with torch.no_grad():
                    servo_pred = servo_model(input_tensor).squeeze(0).numpy() * 1000
                    servo_positions = servo_pred.astype(int)

                set_state("ready_to_move")

                time.sleep(2)

                # Move arm
                for i, servo in enumerate(servosList):
                    arm.setPosition(servo.servo_id, servo_positions[i])

                time.sleep(2)

                arm.setPosition(servo1.servo_id, 300)

                time.sleep(2)

                set_state("ready_to_move")

                time.sleep(2)

                # Draw detection
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, f"{conf:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
