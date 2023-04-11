from messaging.telemetry import Connection
from datetime import datetime
import time, json, uuid, argparse

'''
    mqtt display client mock
'''


parser = argparse.ArgumentParser(description='perform hostile attacks')
parser.add_argument('--hostile', action="store_true", help='publish hostile data')

args = parser.parse_args()


message = {
    'secret_token': 123
}

INIT = 0
AWAKE = 1
CONNECTED = 2

class Client:
    def __init__(self):
        self.startupTimestamp = datetime.timestamp(datetime.now())
        self.id = str(uuid.uuid4())
        self.displayName = "Device 1"
        self.displayType = "display:platform:1"
        
        self.status = INIT
        
        self.conn = Connection("87.94.149.204", 1883)
    
    def connect(self):
        print("connecting...")
        self.conn.connect()
        self.conn.set_user_data(json.dumps(message))
        self.conn.subscribe_multiple([
        
            ("station/PSL/#", lambda res, user, message:(
                print("DATA STATION"),
                print(message.topic),
                print(message.payload.decode()),
                print()
            )),
            
            ("management", lambda res, user, message:(
                self.startup() if message.topic == "rollcall" else self.acknowledge(message.payload) if message.topic == "ack" else None,
                print("MANAGEMENT MESSAGE RECEIVED"),
                print(message.topic),
                print(message.payload.decode()),
                print()
            )),
            
            (f"management/{self.id}", lambda res, user, message:(
                print("SPECIAL MESSAGE FOR ME RECEIVED"),
                print(message.topic),
                print(message.payload.decode()),
                print()
            ))
        ])
        
        if args.hostile:
            self.publish_hostile()
        else:
            self.startup()
            
        
        
    def publish_hostile(self):
        print("publishing hostile data")
        self.conn.publish("management",
            json.dumps({
            "event": "startup",
            "messageTimestamp": 1679886498,
            "message": {
                "uuid": self.id,
                'display_name': self.displayName,
                'display_type': self.displayType,
                'startTimestamp': 1679886498,
            }})
        )
        
        
    def acknowledge(self, payload):
        print("ACKNOLWDGED", payload)
        self.status = CONNECTED
        
    def startup(self):
        print("starting up...")
        
        self.conn.publish("management",
            json.dumps({
            "event": "startup",
            "messageTimestamp": datetime.timestamp(datetime.now()),
            "message": {
                "uuid": self.id,
                'display_name': self.displayName,
                'display_type': self.displayType,
                'startTimestamp': self.startupTimestamp,
            }})
        )
        
        self.status = AWAKE
        
    
   



if __name__ == '__main__':

    try:
        
       
        client = Client()
        client.connect()
        
        while True: time.sleep(100)
       
        
    except Exception as ex:
        print(ex)
        client.conn.disconnect()
        
        
       