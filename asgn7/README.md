# W251 - HW3

## MQTT Topics
I decided to create 2 total MQTT topics consisting of **faces/detect** for the edge MQTT broker and **faces/store** for the cloud MQTT broker.  These topics consist of the base topic faces and a sub topic pertaining to the action of the application.  For the edge, we are simply detecting faces and pushing them to the broker.  For the cloud, we are simply taking the message contents and saving it to IBM Object Storage.

## QoS
I decided to use QoS level 0 since level 1 would allow for duplicate faces to be sent in which case we would have overrepresented datapoints (e.g. faces) in our dataset.  QoS 2 is more demanding from a network standpoint, although it is not currently a limiting constraint for the assignment but may be in future assignments.  Qos level 0 may drop a few faces detected, but we are detectng on a per frame basis so there will be plenty of extremely close replicas that will also be sent even if all of the messages for the previous frame fail.  

## IBM Object Storage HTTP Link
https://s3.us-east.cloud-object-storage.appdomain.cloud/bpc-mids-w251-2
