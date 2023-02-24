import paho.mqtt.client as paho
import os

display = None
MQTT_TOPIC = []


# Is called on every new MQTT message
def onMessage(client, data, msg):
    global display
    global MQTT_TOPIC
    if msg.topic == MQTT_TOPIC[0][0]:
        display.printDisplay(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC[1][0]:
        display.printWarning(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC[2][0]:
        display.printNotification(msg.payload.decode())


def onConnect(client, userdata, flags, rc):
    if rc != 0:
        print("Connection failed: ", rc)


client = paho.Client()
client.on_message = onMessage
client.on_connect = onConnect


def createConnection(topic, new_display):
    global display
    display = new_display
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Current topic: {topic}")
    print("Display initialized. CTRL + C to exit")

    global MQTT_TOPIC
    MQTT_TOPIC = [(topic, 1),
                  ("station/" + display.station + "/warning", 1),
                  ("station/" + display.station + "/notification", 1)]

    client.connect("localhost", 1883, 60)
    client.subscribe(MQTT_TOPIC)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
