import json
from datetime import datetime
import messaging.ratatraffic as rata
from messaging.telemetry import Connection 
from utils.database.sqlite import PersistentConnection
import utils.database.model.display as dao
import configparser
from managementNode import station_names

config = configparser.ConfigParser()
config.read('config.ini')
dbconnection = PersistentConnection()


ADDR = config.get('mqtt-broker', 'ip')
PORT = config.getint('mqtt-broker', 'port')
STATION = 'PSL'

# select the desired keys from the top-level list
t_filter = ['trainType', 'trainCategory', 'commuterLineID']

# select the desired keys from  the 'timeTableRows' list
tt_filter = ['type', 'cancelled', 'scheduledTime', 'differenceInMinutes', 'liveEstimateTime', 'commercialTrack', 'cause']

list_of_stations = station_names.get_station_names()

class Manager:
    def __init__(self):
        self.conn = Connection(ADDR, PORT)
        self.conn.client.on_connect = self.on_connect
        
        
        self.aggregation()
        self.conn.connect()

    def on_connect(self, client, userdata, flags, rc):
        self.conn.on_connect(client, userdata, flags, rc)

        self.conn.subscribe("management", lambda client, userdata, message : (
            payload := json.loads(message.payload.decode('utf-8')),
            print("A device handshake from ", payload['event']),
            self.register_display(payload) if payload['event'] == 'startup' else None

        ))

        ''' I am awake, let's do a rollcall '''
        self.conn.publish("management", json.dumps({
            "event": "rollcall",
            "messageTimeStamp": datetime.timestamp(datetime.now())
        }))
        '''should receive this 

        self.conn.publish("management", json.dumps({
            "event": "startup",
            "messageTimestamp": datetime.timestamp(datetime.now())
            "message": {
                "uuid": "ferf3-ergjo4-98thfs7",
                'display_name': "display#100",
                'display_type': 'display:platform:1',
                'startTimestamp': "324242424.3224",
            },
            
        }))
        '''



    def get_displayinfo(self):
        ''' Get currently known displays from db '''
        with PersistentConnection() as (conn, cur):
            display = dao.Display(conn=conn)
            display.schema()
            
            dinfo = display.fetchall()
            if dinfo:
                return dinfo

            return None


    
    def register_display(self, data):
        '''
            when manager receives "startup" event, it attempts to save the information from the display and send back 'ack' event message (Acknowledged)
        '''
        with PersistentConnection() as (conn, cur):
            display = dao.Display(conn=conn)
            display.schema()

            info = data['message']
            args = (info['uuid'], info['display_name'], info['display_type'], dao.CONNECTED , data['messageTimestamp'], info['startTimestamp'])

            display.insert(*args)

            if cur.rowcount == 0:
                 display.update(*args)
            else:
                # confirm registraction
                print("acknowledged display: ", info['uuid'])
                self.conn.publish(f"management/{info['uuid']}", json.dumps({
                    "event": "ack",
                    "messageTimestamp": datetime.timestamp(datetime.now())
                }))
                
            


    def publish(self, trains):
        for train in trains:
            for shift in train['timeTableRows']:
                platform_id = shift.get('commercialTrack', '?')
                transit = shift.get('type')
                transport_type = train.get('trainCategory')
            
                topic = f"station/{STATION}/{platform_id}/{transit}/{transport_type}"
                self.conn.publish(topic, json.dumps(train))

       #TODO: Check P & I trains for double arrival/departure at same station
    @staticmethod
    def parse(response):
        filtered = {key: response[key] for key in t_filter}
        filtered["allStops"] = []

        #Adding list of all the stops
        for station in response["timeTableRows"]:

            station_short_code = station["stationShortCode"]
            station_name = station_names.get_station_name(station_short_code, list_of_stations)
            filtered["allStops"].append(station_name)

        filtered["allStops"] = list(dict.fromkeys(filtered["allStops"]))
        #Assigning destination for the train
        i = len(filtered["allStops"])-1
        destination = filtered["allStops"][i]

        filtered["destination"] = destination
        filtered["timeTableRows"] = [{key: row.get(key, None) for key in tt_filter} for row in response['timeTableRows'] if row['stationShortCode'] == STATION]

        print(filtered["destination"])
        print(filtered["allStops"])
        return filtered


    def aggregation(self):
        self.trains = rata.Simple('live-trains/station/' + STATION).get(payload={
            'minutes_before_departure': 60,
            'minutes_after_departure': 0,
            'minutes_before_arrival' : 0,
            'minutes_after_arrival': 0,
            'train_categories' : 'Commuter,Long-distance'
        }).onSuccess(lambda response, status, data : (
            filtered := [(self.parse(train)) for train in response.json()],
            self.publish(filtered)
        ))
