#W251 - HW3

##MQTT Topics
I decided to create 2 total MQTT topics consisting of **faces/detect** for the edge MQTT broker and **faces/store** for the cloud MQTT broker.  These topics consist of the base topic faces and a sub topic pertaining to the action of the application.  For the edge, we are simply detecting faces and pushing them to the broker.  For the cloud, we are simply taking the message contents and saving it to IBM Object Storage.

##QoS
I decided to use QoS level 2 since level 0 would possibly result in lost faces for model training in future assignments.  Additionally, level 1 would allow for duplicate faces to be sent in which case we would have overrepresented datapoints (e.g. faces) in our dataset.  While QoS 2 is more demanding from a network standpoint, this is not currently a limiting constraint for the assignment but may be worth considering in the future.  

##IBM Object Storage HTTP Link
https://s3.us-east.cloud-object-storage.appdomain.cloud/bpc-mids-w251-2
