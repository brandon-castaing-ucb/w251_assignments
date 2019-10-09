import numpy as np
import cv2
import base64
from datetime import datetime
from facenet_pytorch import MTCNN
from PIL import Image, ImageDraw
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("faces/detect")

def on_publish(client, userdata, result):
    print("Message published: " + str(result))

# Load face classifier, video camera, and MQTT client
face_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect("mosquitto", 1883, 60)

# Get Nvidia GPU if available
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Create gray image
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Check for faces
    mtcnn = MTCNN(keep_all=True, device=device)
    faces, _ = mtcnn.detect(frame)
    face_count = len(faces)

    # Draw faces
    frame_draw = frame.copy()
    detect_image = ImageDraw.Draw(frame_draw)
    for face in faces:
        detect_image.rectangle(face.tolist(), outline=(255, 255, 255), width=4)

    # Only send images with faces
    if face_count > 0:
        gray_jpg = cv2.imencode('.jpg', detect_image)[1]
        cv2.imwrite("face-"+str(datetime.now())+".jpg", detect_image)
        gray_text = base64.b64encode(detect_image)

        pub_resp = client.publish("faces/detect", gray_text)
        print("Publish response: " + str(pub_resp))
