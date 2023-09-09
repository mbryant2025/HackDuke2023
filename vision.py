# This script uses the USB camera to detect movement and saves the raw image and movement image to the images folder


import cv2
import json

MOTION_MIN = 3
"""Motion threshold. If the average pixel value of the diff image is greater than this value, then there was significant motion"""

cap = cv2.VideoCapture(0)


def get_frame():
    _, img = cap.read()

    return img

def frame_diff(frame1, frame2):
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(frame1, frame2)

    return diff

def get_temp():
    # TODO
    # Fake temperature reading (farhenheit)
    # Return random number between 50 and 120
    return 69


def highlight_motion(frame, diff):
    # Overlay the diff image onto the original image with the diff in red
    
    # Make a copy of the original image
    frame_copy = frame.copy()

    # Make a mask of the diff image
    _, mask = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)

    # Apply the mask to the copy of the original image
    frame_copy[mask > 230] = [0,0,255]

    return frame_copy


def detect_motion(frame):
     # Inputs a diff frame and determines if there was significant motion
     
     # Calculate the average pixel value of the diff image
    avg = cv2.mean(frame)[0]

    # If the average pixel value is greater than MOTION_MIN, then there was significant motion
    if avg > MOTION_MIN:
        return True
    
    return False


def trigger_motion(motion):
     # Write to the json file that motion was detected
     # File is "./data/motion.json"

     with open("./data/motion.json", "w") as f:
        json.dump({"motion": motion}, f)


def main():
      
      prev_frame = get_frame()
      motion_currently_detected = False

      while 1:
            
            frame = get_frame()
            
            diff = frame_diff(prev_frame, frame)

            diff_red = highlight_motion(frame, diff)

            cv2.imshow("Image", diff_red)

            d = detect_motion(diff)

            # If motion_currently_detected is different than d, we need to update the json file
            if motion_currently_detected != d:
                trigger_motion(d)
                motion_currently_detected = d


            prev_frame = frame
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                  break
main()