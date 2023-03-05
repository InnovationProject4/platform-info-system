import paho.mqtt.client as paho
import os
import uuid

display = None
MQTT_TOPIC = []


# Is called on every new MQTT message
def onMessage(client, data, msg):
    global display
    global MQTT_TOPIC

    if msg.topic == "station/" + display.station + "/warning":
        display.printWarning(msg.payload.decode())

    elif msg.topic == "station/" + display.station + "/notification":
        display.printNotification(msg.payload.decode())

    elif display.getType() == 'MAIN':
        if msg.topic == "station/" + display.station + "/main":
            display.printDisplay(msg.payload.decode())

    elif display.getType() == 'DUAL_PLATFORM':  # Only dual platforms have 2 displays
        if msg.topic == display.getTopic()[0]:
            display.printDisplay(msg.payload.decode())
        elif msg.topic == display.getTopic()[1]:
            display.printDisplay2(msg.payload.decode())

    elif display.getType() == 'PLATFORM':  # Only platform displays alert passing trains
        if msg.topic == "station/" + display.station + "/" + display.platform_number:
            display.printDisplay(msg.payload.decode())
        if msg.topic == "station/" + display.station + "/" + display.platform_number + "/passing":
            display.printPassingTrain(msg.payload.decode())


def onConnect(client, userdata, flags, rc):
    if rc != 0:
        print("Connection failed: ", rc)


# UUID used for random client id
new_uuid = str(uuid.uuid4())
client = paho.Client(client_id=new_uuid)
client.on_message = onMessage
client.on_connect = onConnect

client.publish(f'display/{new_uuid}', new_uuid, 1)


def createConnection(topic, new_display):
    global display
    display = new_display

    os.system('cls' if os.name == 'nt' else 'clear')

    global MQTT_TOPIC
    MQTT_TOPIC = [("station/" + display.station + "/warning", 1),
                  ("station/" + display.station + "/notification", 1)]
    MQTT_TOPIC.extend(topic)

    print(f"Current topics: {MQTT_TOPIC}")
    print("Display initialized. CTRL + C to exit")

    client.connect("localhost", 1883, 60)
    client.subscribe(MQTT_TOPIC)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
