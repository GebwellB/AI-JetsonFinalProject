# AI Powered 6-Axis Robot Arm Puzzle Solver
This project is focused around training two models to work together, in an effort to detect, pickup and place a wooden puzzle piece into its designated area.

This is done using an objected detection model and a vision based pose estimated model. Once the objected detection model detects the object, the vision based pose model attempts to move the robot arm into position and attempts to pickup the puzzle piece.

That's the goal of the project. My project, does not do that. Mine, detects the object, attempts to move to that location, but is unable to fully grasp the object and fails to pick it up.

# Instructions:
1. Clone this repo
<pre>git clone https://github.com/GebwellB/AI-JetsonFinalProject</pre>
2. Create a virtual environment and install the requirements
<pre>pip install -r requirements.txt</pre>
3. Place the Number 4 puzzle piece somewhere in line of the camera and in range of the robot arm
4. Run "arm_pickup.py" in "/Robot Arm"
5. Watch as the arm attempts to pickup the Number 4 wooden toy!

# Hardware:
* This project uses the following hardware:
    * xArm 1S. (This needs to be connected via USB to the PC running the arm_pickup.py file)
    * USB Webcam (Connected to the same PC)

# Software Requirements:
* An IDE to run arm_pickup.py. This project used Visual Studio Code

# Additional Notes:
### In this repo, you will find:
1. **Project files** (/Image Training) - This contains both the Number 4 training folder and the Puzzle Numbers training (the image dataset), but I only trained on JUST the number 4. Everything in the Number 4 folder contains base images, my image augmentation and some results based on the number of images I fed into training.

2. **Notebooks** (/Notebooks/Ben's Notebooks) - The 3 notebooks in here are what I used to train my object detection as well as the arm positions based on object detection. These are not tidy, and a lot of stuff was cut out during development because it just didn't work (should really have kept it, but it bugged me too much). The data_collection_THIS_ONE notebook is what I was using to get the the Jetbot to talk to the arm, but gave up on that. The other two (test & FixMaybe) were me trying to find other ways to get the Jetbot to talk to the arm, but, that also led nowhere.

3. **Dataset** - The images I used to train my model are all in: /Image Training/Number 4/augmented_images. These were all generated from 2 base images, located here: /Image Training/Number 4/input_images_base. I tried Roboflow to get these augmentations, but my trail ran out and I couldn't be bothered going through the process of making a new gmail account and getting ANOTHER free trial, so instead I used an image generation python script (/Image Training/Number 4/image_generator.py). This file took the two images in the base folder and applied a bunch of augmentation to them. All of the robot arm position training images are located here: /Robot Arm/Arm Training/. This is a very heavily biases dataset, with me only rotating the image in the same spot, but it did end up working and the two models did allow the arm to move, just... not where I wanted it to go.

4. **Supporting Evidence** - In the Screenshots folder, is a video of the robot arm attempting to pickup the number 4 after it was detected. The folder is mainly used to host the images in the template.md file. Given my trained model, it isn't very good, but you can see it isn't hard coded and does attempt to move roughly to where the piece is. Alas, I don't have any other videos of the data collection process or working inference demos. 