import paho.mqtt.client as paho
import sys
import os

display = None

# Is called on every new MQTT message
def onMessage(client, data, msg):
    global display
    display.printDisplay(msg.payload.decode())

client = paho.Client()
client.on_message = onMessage

if client.connect("localhost", 1883, 60) != 0:
    print("Error in connection")
    sys.exit(-1)

def createConnection(topic, new_display):
    global display
    display = new_display
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Current topic: {topic}")
    print("Display initialized. CTRL + Z to exit")

    client.subscribe(topic)

    try:
        client.loop_forever()
    except:
        client.disconnect()
        print("Error has occured")



