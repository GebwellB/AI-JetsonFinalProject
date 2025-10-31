import ipywidgets
import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display
from jupyter_clickable_image_widget import ClickableImageWidget

# Camera and Motor Interface for JetBot
from jetbot import Robot, Camera, bgr8_to_jpeg

# Basic Python packages for image annotation
from uuid import uuid1
import numpy as np

camera = Camera()

camera_widget = ClickableImageWidget(width=camera.width, height=camera.height)
snapshot_widget = ipywidgets.Image(width=camera.width, height=camera.height)

print(type(camera))

traitlets.dlink((camera, 'value'), (camera_widget, 'value'), transform=bgr8_to_jpeg)