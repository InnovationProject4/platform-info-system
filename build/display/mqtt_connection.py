import paho.mqtt.client as paho
import os
import uuid

display = None


# Is called on every new MQTT message
def onMessage(client, data, msg):
    global display

    if "/warning" in msg.topic:
        display.printWarning(msg)

    elif "/notification" in msg.topic:
        display.printNotification(msg)

    elif "/passing" in msg.topic:
        display.printPassingTrain(msg)

    else:
        display.printDisplay(msg)


def onConnect(client, userdata, flags, rc):
    if rc != 0:
        print("Connection failed: ", rc)


# UUID used for random client id
new_uuid = str(uuid.uuid4())
client = paho.Client(client_id=new_uuid)
client.on_message = onMessage
client.on_connect = onConnect

client.publish(f'display/{new_uuid}', new_uuid, 1)


def createConnection(topics, new_display):
    global display
    display = new_display

    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"Current topics: {topics}")
    print("Display initialized. CTRL + C to exit")

    client.connect("localhost", 1883, 60)
    client.subscribe(topics)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
