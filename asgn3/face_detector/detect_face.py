import numpy as np
import cv2
import time
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

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Create gray image
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Check for faces
    faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
    face_count = len(faces)
    print("Found " + str(face_count) + " in this frame.")

    # Draw rectangle around face
    for (x,y,w,h) in faces:
        cv2.rectangle(gray_img, (x,y), (x+w, y+h), (255,0,0), 2)
    
    # Only send images with faces
    if face_count > 0:
        image_title = "face-" + str(time.time()) + ".jpg"
        gray_str = cv2.imencode(image_title, gray_img)[1].tostring()
        
        pub_resp = client.publish("faces/detect", gray_str, 2)
        print("Publish response: " + str(pub_resp))
