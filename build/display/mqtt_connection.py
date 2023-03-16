import uuid

from messaging.telemetry import Connection

display = None
conn = Connection("localhost", 1883)
new_uuid = str(uuid.uuid4())


def createConnection(new_display):
    global display
    display = new_display
    # Last will message if connection disconnects without disconnect()
    conn.set_last_will(f"management/{new_uuid}", f"Disconnected: {new_uuid}", 0)
    conn.connect()

    conn.publish(f"management/{new_uuid}", f"Connected: {new_uuid}")
    conn.subscribe_multiple(display.handleSubscriptions())


# Is called when the Tkinter root window is closed
def onDisconnect():
    conn.publish(f"management/{new_uuid}", f"Disconnected: {new_uuid}")
    conn.disconnect()  # Here last will message is not published
