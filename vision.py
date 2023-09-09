# This script uses the USB camera to detect movement and saves the raw image and movement image to the images folder


import random
import cv2


cap = cv2.VideoCapture(0)


def get_frame():
    _, img = cap.read()

    return img

def frame_diff(frame1, frame2):
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(frame1, frame2)

    return diff


def highlight_motion(frame, diff):
    # Overlay the diff image onto the original image with the diff in red
    
    # Make a copy of the original image
    frame_copy = frame.copy()

    # Make a mask of the diff image
    _, mask = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)

    # Apply the mask to the copy of the original image
    frame_copy[mask > 50] = [0, 0, 255]

    return frame_copy







def main():
      
      prev_frame = get_frame()

      while 1:
            
            frame = get_frame()
            
            diff = frame_diff(prev_frame, frame)

            diff2 = highlight_motion(frame, diff)

            cv2.imshow("Image", diff)
            cv2.imshow("Image", diff2)


            prev_frame = frame
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                  break
            
    # cap.release()
    # cv2.destroyAllWindows() 
      

main()
            



# while True:
#         # get and display next frame
#         img = get_frame()
#         cv2.imshow("Image", img)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
