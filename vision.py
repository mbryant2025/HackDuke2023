from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

MOTION_MIN = 1.5

motion_currently_detected = False
temp = 98
humid = 69
consecutive_danger = 0

MIN_DANGER_FRAMES = 6
HIGH_DANGER_TEMP = 100
LOW_DANGER_TEMP = 90

def frame_diff(frame1, frame2):
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(frame1, frame2)
    return diff

def highlight_motion(frame, diff):
    frame_copy = frame.copy()
    _, mask = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)
    frame_copy[mask > 230] = [0, 0, 255]
    return frame_copy

def detect_motion(frame):
    avg = cv2.mean(frame)[0]
    if avg > MOTION_MIN:
        return True
    return False
    # # We say that motion is detected if there are more than 30 white pixels in a 10x10 grid
    # # Use kernel to count number of white pixels in each 10x10 grid
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))

    # # Apply kernel to frame
    # dilated = cv2.dilate(frame, kernel)

    # # Determine the maximum pixel value in the frame
    # max_pixel = cv2.max(dilated)
    # # global temp
    # # temp = max_pixel
    # # If the maximum pixel value is greater than 230, then motion is detected
    # if max_pixel > 230:
    #     return True
    # return False




def generate_frames():

    global motion_currently_detected

    cap = cv2.VideoCapture(0)
    prev_frame = cap.read()[1]

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:

            # Do motion detection
            diff = frame_diff(prev_frame, frame)
            diff_red = highlight_motion(frame, diff)

            # Update previous frame
            prev_frame = frame.copy()

            motion_currently_detected = detect_motion(diff)

            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', diff_red)
            if not ret:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Transmit data representing the current state of motion detection
@app.route('/motion')
def motion():
    return str(motion_currently_detected)

@app.route('/temperature')
def temperature():
    return str(temp)

@app.route('/humidity')
def humidity():
    return str(humid)

@app.route('/alert')
def alert():
    global consecutive_danger
    if motion_currently_detected:
        consecutive_danger += 1
    else:
        consecutive_danger = 0

    if consecutive_danger > MIN_DANGER_FRAMES:
        return 'ALERT: Patient Movement Detected'
    elif temp > HIGH_DANGER_TEMP or temp < LOW_DANGER_TEMP:
        return 'ALERT: Patient Temperature Critical'
    else:
        return 'Patient at Rest or Deceased'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
