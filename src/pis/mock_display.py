from pis.messaging.telemetry import Connection
from datetime import datetime
import time, json, uuid, argparse

'''
    mqtt display client mock
'''


parser = argparse.ArgumentParser(description='perform hostile attacks')
parser.add_argument('--hostile', action="store_true", help='publish hostile data')

args = parser.parse_args()

def color(text, color, optional=None):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "light_gray": "\033[37m",
        "dark_gray": "\033[90m",
        "light_red": "\033[38;5;9m",
        "light_blue": "\033[38;5;75m",
        "light_cyan": "\033[38;5;14m",
        "end": "\033[0m"
    }
    if text is None: 
        if optional is None: optional = color
        return colors[optional] + "None" + colors["end"]
    else: return colors[color] + text + colors['end']


topic = "station/PSL/6/DEPARTURE/Long-distance"
message = """

station/PSL/6/DEPARTURE/Long-distance
{"messageTimestamp": "2023-04-18T07:06:19.187595Z", "stationFullname": "Helsinki", "schedule": [{"id": 140579130596160, "train_id": 44, "type": "DEPARTURE", "cancelled": false, "scheduledTime": "2023-04-18T07:49:00.000Z", "differenceInMinutes": 0, "liveEstimateTime": "2023-04-18T07:49:14.000Z", "actualTime": null, "commercialTrack": "6", "trainStopping": true, "cause": null, "destination": "Helsinki asema", "stopOnStations": ["Helsinki asema"], "commuterLineID": "S44"}]}42bf8965ef38be51fb3d86946d293974a2d58d65c85b6866c83839d3ebb1b5e10ddd153b9020f7af3c0c194c04d87c866a5cefbec526d1d4a68215b72036cb5306aa761499f57dcdb5b8e136651259ff1fa3c6c0005943edad0abe3fca6c58c69f2b795213e51e8a4429861aa0877585798d851424ae944a41084e353bb64e8d80fb1985178754e17b6d6650f450809bdb8934bcf5f56f715a28a93027f1a2c090c65d6f241764a16e57b9c7818863d3d38c6f1684d202cd648484b08227017962d9857d3466ca63a063885bdea0c6a13fb129359c437dd584216de8024aef69b1c9f1b9b2537a811f03d5ca3ee03a0a510911e9a40d8d9a691d630fd5120b27






"""

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
        
            ("station/EPO/#", lambda res, user, message:(
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
                print("DIRECT MESSAGE FOR ME"),
                print(message.topic),
                print(message.payload.decode()),
                print()
            )),
            
            
            (f"management/+", lambda res, user, message:(
                print("DIRECT HIJACKED MESSAGE"),
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
        self.conn.publish(topic, message.strip())
        
        
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
        
    
   
def main():
    try:
        client = Client()
        client.connect()
        while True: time.sleep(100)
       
        
    except Exception as ex:
        print(ex)
        client.conn.disconnect()


if __name__ == '__main__':
    main()
        
        
       