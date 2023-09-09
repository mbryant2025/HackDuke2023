from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

MOTION_MIN = 3

motion_currently_detected = False

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

if __name__ == "__main__":
    app.run(debug=True)
