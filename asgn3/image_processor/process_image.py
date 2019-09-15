import numpy as np
import cv2
import base64
from datetime import datetime
import paho.mqtt.client as mqtt
import ibm_boto3
from ibm_botocore.client import Config, ClientError

# Insecure, but trying to finish assignment before the deadline.
bucket_hash = {
  "apikey": "OBFUSCATED_FOR_GIT_PUSH",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/d9bb57eeeae440448da30b78af11846a:302ad5ed-98fd-4707-8d32-1d0d7113e985::"
}

client = ibm_boto3.client('s3')

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=bucket_hash['apikey'],
    ibm_service_instance_id=bucket_hash['resource_instance_id'],
    ibm_auth_endpoint="https://iam.cloud.ibm.com/identity/token",
    config=Config(signature_version="oauth"),
    endpoint_url='https://s3.us-east.cloud-object-storage.appdomain.cloud'
)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("faces/store")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Message receive on " + msg.topic + ": " + str(msg.payload)[:30])

    jpg_as_np = np.frombuffer(base64.b64decode(msg.payload), dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)

    img_name = 'face-' + datetime.now().strftime("%m_%d_%YT%H_%M_%S") + '.jpg'
    cv2.imwrite(img_name, img)

    try:
        resp = cos.meta.client.upload_file(Filename=img_name, Bucket='bpc-mids-w251-2', Key=img_name)
        print("IBM S3 response: " + str(resp))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create text file: {0}".format(e))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("50.23.146.138", 1883, 60)

client.loop_forever()
