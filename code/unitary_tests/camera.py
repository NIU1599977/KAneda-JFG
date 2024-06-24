from flask import Flask, Response
import io
from picamera2 import Picamera2, MappedArray
import cv2

app = Flask(__name__)

def gen():
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": (320, 240)}, controls={"FrameRate": 24})
    picam2.configure(config)
    picam2.start()

    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)  # Encode the frame as JPEG
        frame_data = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<h1>Raspberry Pi Camera Streaming</h1><p>Go to <a href='/video_feed'>/video_feed</a> to see the camera stream.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
