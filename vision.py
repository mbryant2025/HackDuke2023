# This script uses the USB camera to detect movement and saves the raw image and movement image to the images folder

import cv2

previous_frame = None # Gray scale image of the previous frame

# Stream from the camera
def get_frame(camera):
    # Read the frame from the camera
    _, frame = camera.read()
    # Convert the frame to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Save it as the previous frame
    global previous_frame


    