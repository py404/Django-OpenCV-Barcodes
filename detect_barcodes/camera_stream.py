import os

import cv2
import numpy
from pyzbar.pyzbar import decode


class CameraStream:
    def __init__(self):
        self.camera = cv2.VideoCapture(int(os.environ.get('CAMERA')))

    def get_frames(self):
        while True:
            # Capture frame-by-frame
            success, frame = self.camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

