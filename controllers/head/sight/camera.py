__author__ = "Mohammad Dabiri"
__copyright__ = "Free to use, copy and modify"
__credits__ = ["Mohammad Dabiri"]
__license__ = "MIT Licence"
__version__ = "0.0.1"
__maintainer__ = "Mohammad Dabiri"
__email__ = "moddabiri@yahoo.com"

import picamera
from PIL import Image
import cv2
import os   
from cv2 import face

camera_temp_capture = '/tmp/picamera_capture.jpg'
capture_resolution = (640, 480)

current_dir = os.path.dirname(os.path.abspath(__file__))

cascadePath = os.path.join(current_dir, "haarcascade_frontalface_default.xml")
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = face.createLBPHFaceRecognizer(radius=1, neighbors=16, grid_x=32, grid_y=32)
#recognizer.load(os.path.join(current_dir, 'trained_model.xml'))

def capture():
    #Capture
    try:
        camera = picamera.PiCamera()
        camera.resolution = capture_resolution
        camera.capture(camera_temp_capture)
    except Exception as ex:
        my_print("Failed to capture: %s"%ex)
    finally:
        camera.close()

def detect():
    #Detection
    predict_image_pil = Image.open(camera_temp_capture).convert('L')    
    predict_image = np.array(predict_image_pil, 'uint8')
    
    #predict_image = cv2.cvtColor(predict_image, cv2.COLOR_BGR2GRAY)
    return faceCascade.detectMultiScale(predict_image)

def recognize(faces):
    recognized = []
    #Recognize
    for (x, y, w, h) in faces:
        face_id = recognizer.predict(predict_image[y: y + h, x: x + w])

        if face_id:
            recognized.append(face_id)

    return recognized

