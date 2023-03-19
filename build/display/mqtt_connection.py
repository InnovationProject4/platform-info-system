import sys
import uuid
import configparser
from messaging.telemetry import Connection

config = configparser.ConfigParser()
config.read('config.ini')
display = None

ip = config.get('mqtt-broker', 'ip')
port = config.get('mqtt-broker', 'port')
conn = Connection(ip, int(port))
new_uuid = str(uuid.uuid4())



def createConnection(new_display):
    global display
    display = new_display
    # Last will message if connection disconnects without disconnect()
    conn.set_last_will(f"management/{new_uuid}", f"Disconnected: {new_uuid}", 0)

    try:
        conn.connect()
    except ConnectionRefusedError:
        print("Connection to the broker failed")
        sys.exit()

    conn.publish(f"management/{new_uuid}", f"Connected: {new_uuid}")
    conn.subscribe_multiple(display.handleSubscriptions())


# Is called when the Tkinter root window is closed
def onDisconnect():
    conn.publish(f"management/{new_uuid}", f"Disconnected: {new_uuid}")
    conn.disconnect()  # Here last will message is not published
