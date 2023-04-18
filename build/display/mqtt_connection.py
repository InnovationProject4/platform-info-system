import json
import sys
import uuid
from datetime import datetime
from messaging.telemetry import Connection
import display.display_printer as dp

import utils.conf as conf
import utils.integrity as integrity


display = None
typeof = None

conn = Connection(conf.ADDR, int(conf.PORT))
new_uuid = str(uuid.uuid4())
startTimestamp = None

last_will_message = json.dumps({
                     "event": "disconnected",
                     "messageTimestamp": datetime.timestamp(datetime.now()),
                     "message": {
                         "uuid": new_uuid,
                         'startTimestamp': datetime.timestamp(datetime.now())
                     }})


def startup():
    '''  establish connection and send startup message im plain json'''
    
    conn.publish("management",
        json.dumps({
            "event": "startup",
            "messageTimestamp": datetime.timestamp(datetime.now()),
            "message": {
                "uuid": new_uuid,
                'display_name': f"display-{display.station}-{typeof}",
                'display_type': typeof,
                'startTimestamp': startTimestamp
        }})
    )
    
    global reactive_toast
    dp.reactive_toast.value = ["Attempting pairing", "show"]




def acknowledge(payload):
    '''connection established and acknowledged. Important data is shared.'''
    if payload['event'] == 'ack':
        conf.Conf().cert = integrity.load_certificate(integrity.FILETYPE_PEM, payload['message'].encode())
        dp.reactive_toast.value = ["Link established with management node", "success"]
        
    

    # Last will message if connection disconnects without disconnect()
    conn.set_last_will("management", last_will_message, 0)
     
     
     
     
     
def createConnection(new_display, type):
    global display, typeof, startTimestamp
    
    display = new_display
    typeof = type
    
    startTimestamp = datetime.timestamp(datetime.now())

    try:
        conn.connect()
    except ConnectionRefusedError:
        print("Connection to the broker failed")
        sys.exit()
        
    conn.subscribe_multiple([
        ('management', lambda res, user, message: (payload := json.loads(message.payload.decode()), startup() if payload['event'] == 'rollcall' else None)),
        (f'management/{new_uuid}', lambda res, user, message: acknowledge(json.loads(message.payload.decode())))
    ])
    
    startup()

    # Alert the aggregator to publish data from database
    conn.publish(f"management/{new_uuid}/update", "")

    conn.subscribe_multiple(display.handleSubscriptions())




# Is called when the Tkinter root window is closed
def onDisconnect():
    global last_will_message
    conn.publish("management", last_will_message)
    conn.disconnect()  # Here last will message is not published
