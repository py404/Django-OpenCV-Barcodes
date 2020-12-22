from django.http import StreamingHttpResponse
from django.shortcuts import render

from .camera_stream import CameraStream


# Create your views here.
def camera_feed(request):
    stream = CameraStream()
    frames = stream.get_frames()
    return StreamingHttpResponse(frames, content_type='multipart/x-mixed-replace; boundary=frame')


def detect(request):
    stream = CameraStream()
    success, frame = stream.camera.read()
    if success:
        status = True
    else:
        status = False
    return render(request, 'detect_barcodes/detect.html', context={'cam_status': status})
