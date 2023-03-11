from messaging.telemetry import Connection

display = None

# # UUID used for random client id
# new_uuid = str(uuid.uuid4())
# client = paho.Client(client_id=new_uuid)
# client.on_message = onMessage
# client.on_connect = onConnect
#
# client.publish(f'display/{new_uuid}', new_uuid, 1)


def createConnection(new_display):
    global display
    display = new_display

    conn = Connection("localhost", 1883)
    conn.connect()


    try:
        conn.subscribe_multiple(display.handleSubscriptions())
    except KeyboardInterrupt:
        conn.disconnect()
