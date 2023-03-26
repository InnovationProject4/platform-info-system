import json
import sys
import uuid
import configparser
from datetime import datetime

from messaging.telemetry import Connection

config = configparser.ConfigParser()
config.read('config.ini')
display = None

ip = config.get('mqtt-broker', 'ip')
port = config.get('mqtt-broker', 'port')
conn = Connection(ip, int(port))
new_uuid = str(uuid.uuid4())


def createConnection(new_display, type):
    global display
    display = new_display
    # Last will message if connection disconnects without disconnect()
    conn.set_last_will(f"management/{new_uuid}", f"Disconnected: {new_uuid}", 0)

    try:
        conn.connect()
    except ConnectionRefusedError:
        print("Connection to the broker failed")
        sys.exit()

    conn.publish(f"management/{new_uuid}", f"Connected: {new_uuid}\n"
                                           f"- Display: {type}\n"
                                           f"- Station: {new_display.station}")

    conn.publish("management",
                 json.dumps({
                     "event": "startup",
                     "messageTimestamp": datetime.timestamp(datetime.now()),
                     "message": {
                         "uuid": new_uuid,
                         'display_name': f"display-{new_display.station}-{type}",
                         'display_type': type,
                         'startTimestamp': datetime.timestamp(datetime.now())
                     }})
                 )

    # Alert the aggregator to publish data from database
    conn.publish(f"management/{new_uuid}/update", "")

    conn.subscribe_multiple(display.handleSubscriptions())


# Is called when the Tkinter root window is closed
def onDisconnect():
    conn.publish(f"management/{new_uuid}", f"Disconnected: {new_uuid}")
    conn.disconnect()  # Here last will message is not published
