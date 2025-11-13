# Applying CRISP-DM Methodology to the PuzzArm Project

**Document Purpose:**  
This document applies the Cross-Industry Standard Process for Data Mining (CRISP-DM) methodology to the PuzzArm project, structuring the AI/ML components (e.g., image identification for puzzle pieces, pose estimation, and imitation learning for arm control) across its six phases. CRISP-DM provides an iterative, non-linear framework for ML projects, emphasising business alignment and continuous refinement. This application serves as a checkpoint for the clustered AI course, mapping to ICTAII501 (designing AI solutions) and ICTAII502 (implementing ML models).

Use this as Assessment template, filling in project-specific details based on your work (e.g., Roboflow training/Arm training ).

**Project Recap:** PuzzArm is an AI-powered robotic system using Jetson Nano and xArm1S to solve a number puzzle (0-9 pieces), with dual-arm teleop (or similar method) for data collection. The ML focus is on vision-based detection, classification, and motion policies.

**Iteration Note:** CRISP-DM is cyclical—after Deployment, loop back to Business Understanding for refinements (e.g., adding new puzzles).



---

## Phase 1: Business Understanding
**Objective:** Define the problem, goals, and success criteria in business terms. Assess resources and risks.  

- **Business Problem:** Automate puzzle solving to create an educational robotics demo for expo demonstrations  and marketing events.
- **Data Mining Goals:** Develop models for piece detection (~70% accuracy), pose estimation (handling rotations), and arm control (50% pick-place success).  
- **Project Plan:** Timeline (4-6 weeks); resources (Jetson Nano, xArm1S, Roboflow). 
- **Risks:**
	- Imcompatible Python versions between components
  - Hardware failures
  - Detection model fails to detect objects clearly enough
  - Once an object is detected, the arm failing to move to the position correctly
  - Unhandled exceptions in code, causing the arm to not do anything
  - Accuracy not meeting expectations, then causing issues in detecting objects


- **Student Input**:
  - I addressed the business need by focusing on automating the puzzle solving process through integrating computer vision and robotic arm control to create an engaging educational demo. First, I defined clear goals, such as aiming for 70% accuracy in peice detection and aiming for at least 50% pickup rate in the robotic arm in moving and then picking up the puzzle piece. To support these goals, I selected suitable hardware, such as the Jetson Nano for processing and the xArm1S for manipulation. I then used Roboflow to augment images for training. Following augmentation, I continued to use Roboflow to train the model to detect the puzzle pieces.

   *Mapping to Units:** ICTAII501 PC 1.1-1.2 (confirm work brief via CRISP-DM business phase).*

---

## Phase 2: Data Understanding
**Objective:** Collect initial data, explore it, and identify quality issues.  

- **Initial Data Collection:** 100-200 images of puzzle pieces/slots from top-down camera (via Jetson CSI), plus teleop videos (ROS2 bags) for joint states. Sources: Manual photos, Roboflow public datasets for augmentation.  
- **Data Description:** Structure (images: RGB, 224x224; labels: 0-9 classes; joints: 6D floats). Volume: ~5k samples post-augmentation.  
- **Data Exploration:** Use pandas/matplotlib for histograms (e.g., class balance: 10% per digit); identify issues (e.g., lighting bias via correlation plots).  
- **Student Input:** 
  - For my Roboflow dataset, I took an original set of 30 images, fed them through an image augmentor to apply tilt, zoom, grainyness, grey scale, flipped horzontally and vertically and mirrored. This produced over 1300 images from my original 30. From that dataset, I trained the model in Roboflow using 25 test images, 45 valid and 1300 unseen data. From this set, I received an accuracy from the test images of between 30 and 90%, based on orientation and filtering etc. However, I did find during training that I overfed the model in some areas, causing data bias (it favoured the number 4 to be front and centre, and not to the side).

  I did not use any code for this, as it was all done on Roboflow. Below is a screenshot of my trained model stats:
  ![screenshot_of_trained_model_stats](/Screenshots/Roboflow_Trained_Model.PNG)
*Mapping to Units ICTAII502 PC 1.1-1.6 (analyse requirements and data attributes using CRISP-DM data phase).*  

---

## Phase 3: Data Preparation
**Objective:** Clean, transform, and construct the final dataset for modeling.  

- **Data Cleaning:** Remove duplicates/blurry images (OpenCV thresholding); handle missing labels via Roboflow auto-annotation.  
- **Feature Engineering:** Augment for rotations (0-360° via Albumentations); normalize images (0-1 scale); engineer joint deltas from teleop recordings.  
- **Final Dataset:** Train (70%): 3.5k samples; Val (20%): 1k; Test (10%): 500. Format: PyTorch DataLoader for Jetson training.  
- **Student Input:** Using Roboflow, I applied a variety of augmentations including vertical and horizontal flips, brightness adjustments of ±15%, mirroring, grain filtering, tilting, shearing, zooming, cropping, saturation, and exposure changes. These augmentations expanded the diversity of the dataset, helping the model generalise better by exposing it to different orientations, lighting conditions and distortions of the target object. Below are the before and after results of adjusting the augmentation. These preprocessing steps contributed significantly to improving the robustness and accuracy of the model during training.

### Before:
![screenshot_of_before_augmentation](/Screenshots/before-results.PNG)

### After:
![screenshot_of_after_augmentation](/Screenshots/after-results.PNG)

- **Mapping to Units:** ICTAII502 PC 2.1-2.4 (set parameters, engineer features per CRISP-DM prep phase).  

---

## Phase 4: Modeling
**Objective:** Select and apply ML techniques, tuning parameters.  

- **Model Selection:** - Model Name: 204-Number4s (created in Roboflow, trained on Kaggle), uses YOLOv5
- **Techniques Applied:** - Supervised training, data augmentation (vertical and horizontal flips, brightness adjustments of ±15%, mirroring, grain filtering, tilting, shearing, zooming, cropping, saturation, and exposure changes), early stopping to avoid overfitting, data splitting (training, validation and test sets), image resizing to a uniform size
- **Model Building:**  - For my model, I trained detection first, then trained the policy model based on object location and where the robot arm SHOULD be when attempting pickup, then exporting to TensorRT

*Mapping to Units ICTAII502 PC 3.1-3.5 (arrange validation, refine parameters via CRISP-DM modeling).*  

---

## Phase 5: Evaluation
**Objective:** Assess model performance against business goals; review process.  

- **Model Assessment:** - In training, my model achieved a very high, 96% detection rate of the number 4 (the only number I trained). Testing this with a webcam, the actual real-world success was around 60-80%, based on lighting conditions, table colour, anything else in the capture window.

  The policy success rate was more around 10-25% successful. It could detect the object, and the arm would attempt pickup, but due to low training on the policy, the arm failed to achieve it's task of picking up the object. This was due to bias in training where I set arm positions too frequently in the same position, so it always tried to go to a very similar position. However, if the object was further away, the arm did attempt to move closer towards it, but it struggled to get there. The video below shows how well it performed. In terms of pick / place trials, it attempted serval times, with 0% success rate. This was purely down to my training of the policy. If I had more unbiased data, I'm confident I could get the robot arm to at least hover over the target area, and clamp down to attempt a pickup.
### Detection Success Rate (In training):
![screenshot_of_detection_success](/Screenshots/4-successrate.PNG)

### Video of the robot arm in action:
[Robot arm video](/Screenshots/robot_arm.mov)
- **Business Criteria Check:** Does it enable full puzzle solve <5 min?  - No, not even close. But if more training was done, I'm confident in saying that it can at least move the number 4 to somewhere else on the table, as it was never trained to try and place on the wooden board.
- **Process Review:** Data quality issues? (e.g., rotations fixed via augments). Next iteration: - Data quality for both models was below average. I needed more unbiased data on the number 4, as well as the positions of the object on the table relative to the arms pickup locations. For the next iteration, I would take more photos and apply slightly less augmentation to the images, as that contributed to not having an as accurate image detection. I would also focus on more random locations over the desk for the arm to try and pickup the object, avoiding bias data again.



*Mapping to Units ICTAII502 PC 5.1-5.6 (finalize evaluations, document metrics per CRISP-DM eval phase); ICTAII501 PC 3 (document design outcomes).*  

---

## Phase 6: Deployment
**Objective:** Plan rollout, monitoring, and maintenance.  

- **Deployment Plan:** Ideally, deploying this model on the Jetbot with the arm so the entire project can run through the Jetbot would be my goal, however due to Python version issues and hardware limitations between the arm and the Jetbot, this wasn't possible. But assuming everything **just worked** my deployment plan would be:
  1. Deploy models to the Jetbot
  2. Hook up arm / webcam to the Jetbot
  3. Run code and test pickup / placement
  4. Final deployment / handover
- **Monitoring:** For monitoring, I would log the following metrics, for a base line:
  1. How long it took to detect the object
  2. How long it took before it attempted to move to the object and attempted pickup
  3. How long it took reset after placing the object
  
      These three points offer valuable insight to help retrain and aim for a faster, more reliable model in the next iteration. A quartly retrain with new data will also greatly help the models accurary going forward.
- **Business Reporting:** 

  This is the demo of the robot in action, same as above: [Robot arm video](/Screenshots/robot_arm.mov)

  The models used for this assessment, are located in /Robot Arm/Models. Labelled as V1.0 as they are the first iteration. Going forward, this would contain the different model names and version numbers, for historical purposes.

  For the time invested, the model / robot can:

  1. Identify the number 4 relativtly accuratly (60-80% of the time)
  2. Attempt moving to the detected object, but fail to get there, but get sort of in the right area
  3. Reset and try again

*Mapping to Units ICTAII501 PC 2 (design for deployment); ICTAII502 PC 4.1-4.5 (finalize test procedures).*  

---

## Overall Reflection and Iteration Plan
 **Next Steps:** *Student input* - What do you need to do next to achieve the project.  200 -400 words + code samples if required.

 To successfully achieve this project's objectives, I would need more unbiased images for training the detection model, and more training data for the policy model the arm uses. The current model lacks sufficient variety in terms of object location and enviromental context, which greatly limits the models ability to generalise beyond a standard position. This lack of diverse training images results in the model struggling to accurately detect objects when they appear in different places or different orientations.

 To add onto this, the policy model that guides the robotic arms movement also suffers from insufficent training. Without enough exmaples of varying arm positions and picking locations, the model cannot reliable learn the necessary locations to reach and grap onto the objects correctly. Although the current policy model attempts to move the arm towards the object, it often falls short or moves completely in the wrong direction, which proves it needs further refinement.

 To address both of these issues, more extensive data collection is needed, and more importantly, is critical in this type of application. This would involve capturing more images with objects placed in a wide range of random positions across a tabl, preferrably of different backgrounds to avoid bias. Additionally, gathering more varied examples of the arms pickup attempts will provide better context for the policy model, alongside improving data quality, it will also help with optimising the control code, making it quicker at detecting, moving, and picking up objects. With these changes, the next iteration would have a much higher success rate and be much more reliable.

 The code used to test the current model is located in: /Robot Arm/arm_pickup.py - **Disclaimer:** Most of this code is AI generated, as it was needed to test the two models working together. It wouldn't be an AI course without AI generated code! Below is the code:

 ```python
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
 ```