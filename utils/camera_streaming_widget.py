import os
from datetime import datetime

import cv2
import numpy as np
from pyzbar.pyzbar import decode


class CameraStreamingWidget:
    def __init__(self):
        self.camera = cv2.VideoCapture(int(os.environ.get('CAMERA')))
        self.media_path = os.path.join(os.getcwd(), "media", "images")
        # create "media/images" folder if doesn't exist
        if not self.media_path:
            os.mkdir(self.media_path)

    def get_frames(self):
        while True:
            # Capture frame-by-frame
            success, frame = self.camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                
                # Add text on top of the barcode if there is a barcode in the stream using opencv
                # convert camera frame to numpy array
                color_image = np.asanyarray(frame)

                # decode numpy array to check if there is a barcode in color_image
                # you can add a custom check here to verify if the qr code has right identifier information
                if decode(color_image):
                    for barcode in decode(color_image):
                        barcode_data = (barcode.data).decode('utf-8')
                        # if barcode data exists
                        if barcode_data:                            
                            # save file as PNG if a QR code is detected
                            today = str(datetime.now().strftime("%d-%m-%y"))
                            image = os.path.join(self.media_path, f"img_{today}.png")
                            cv2.imwrite(image, frame)
                            
                            # print info for debugging purpose
                            print('-'*50)
                            print('Saving image to media...')
                            print('-'*50)
                            print(f'Saved as: {image}')
                            print('-'*50)
                            
                            pts = np.array([barcode.polygon], np.int32)
                            pts = pts.reshape((-1,1,2))
                            # draw polylines on the barcode
                            cv2.polylines(
                                img=color_image,
                                pts=[pts],
                                isClosed=True,
                                color=(0,255,0),
                                thickness=3
                            )
                            pts2 = barcode.rect
                            # put text on top of polylines
                            barcode_frame = cv2.putText(
                                img=color_image,
                                text=barcode_data,
                                org=(pts2[0], pts2[1]),
                                fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                                fontScale=0.9,
                                color=(0,0,255),
                                thickness=2
                            )
                            # encode the new barcode_frame that has polylines and barcode data text
                            _, buffer_ = cv2.imencode('.jpg', barcode_frame)
                            # convert barcode_frame to bytes
                            barcode_frame = buffer_.tobytes()
                            # yield output stream with polylines and barcode data text
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n\r\n' + barcode_frame + b'\r\n\r\n')
                # else, yield the normal camera stream
                else:
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
