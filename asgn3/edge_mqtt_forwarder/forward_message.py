import paho.mqtt.client as mqtt

def edge_on_connect(client, userdata, flags, rc):
    print("Connected to the edge MQTT with result code: " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("faces/detect")

def cloud_on_connect(client, userdata, flags, rc):
    print("Connected to the cloud MQTT with result code: " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("faces/store", 2)


def edge_on_message(client, userdata, msg):
    print("Hey, look a message was published and received!")
    print(msg.topic + ": " + str(msg.payload))

    print(type(msg.payload))

    print("Publishing message to the cloud...")
    pub_resp = cloud_client.publish("faces/store", msg.payload, 2)
    print("Publish response: " + str(pub_resp))
    

def cloud_on_publish(client, userdata, result):
    print("Message published: " + str(result))


edge_client = mqtt.Client()
edge_client.on_connect = edge_on_connect
edge_client.on_message = edge_on_message
edge_client.connect("mosquitto", 1883, 60)

cloud_client = mqtt.Client()
cloud_client.on_connect = cloud_on_connect
cloud_client.on_publish = cloud_on_publish
cloud_client.connect("50.23.146.138", 1883, 60)

edge_client.loop_forever()
