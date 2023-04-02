import json
from datetime import datetime
import messaging.ratatraffic as rata
from messaging.telemetry import Connection 
from utils.database.sqlite import PersistentConnection
import utils.database.model.display as dao
import configparser
from collections import defaultdict
from managementNode import announcement_manager
from utils.Event import observable

config = configparser.ConfigParser()
config.read('config.ini')
dbconnection = PersistentConnection()


ADDR = config.get('mqtt-broker', 'ip')
PORT = config.getint('mqtt-broker', 'port')

# select the railway stations to filter for using shortStationCodes
targets = []

# select the desired keys from the top-level list
t_filter = ['trainNumber', 'trainType', 'trainCategory', 'commuterLineID']

# select the desired keys from  the 'timeTableRows' list
tt_filter = ['type', 'cancelled', 'scheduledTime', 'differenceInMinutes', 'liveEstimateTime', 'commercialTrack', 'trainStopping', 'cause']

class Manager:
    def __init__(self, stations=[]):
        self.conn = Connection(ADDR, PORT)
        self.conn.client.on_connect = self.on_connect
        
        self.targets = stations
        
        self.aggregation()
        self.conn.connect()

    def on_connect(self, client, userdata, flags, rc):
        self.conn.on_connect(client, userdata, flags, rc)

        self.conn.subscribe_multiple([
            
            ("management", lambda client, userdata, message : (
                payload := json.loads(message.payload.decode('utf-8')),
                print("A device handshake from ", payload['event']),
                self.register_display(payload) if payload['event'] == 'startup' else None
            )),
            
            
            ("management/+/update", lambda client, userdata, messages: (
                announcement_manager.publishAnnouncements(self.conn)
            ))
            
        ])
        
        
        
        ''' I am awake, let's do a rollcall '''
        self.conn.publish("management", json.dumps({
            "event": "rollcall",
            "messageTimeStamp": datetime.timestamp(datetime.now())
        }))

    def get_displayinfo(self):
        ''' Get currently known displays from db '''
        with PersistentConnection() as (conn, cur):
            display = dao.Display(conn=conn)
            display.schema()
            
            dinfo = display.fetchall()
            if dinfo:
                return dinfo
            
            

            return dinfo
        
        
    # TODO 1110 lines of data, consider using B-tree
    def get_full_stationname(self, code):
        if self.station_codes is not None:
            for station in self.station_codes:
                if station["stationShortCode"] == code:
                    return station["stationName"]
            else:
                print("No such station code in the dictionary.")
                return code
        


    
    def register_display(self, data):
        '''
            when manager receives "startup" event, it attempts to save the information from the display and send back 'ack' event message (Acknowledged)
        '''
        # TODO REPLACE PERSISTENT MEMORY WITH CONNECTION() AS FILE
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
                
    
    
    def pub(self, rows, station):
        trains_baseinfo, schedules = rows
        
        for topic, trains in schedules.items():
            responseData = defaultdict(list)
             
            for train_id, schedule in trains.items():
                train_info = trains_baseinfo[train_id]
                    
                t = train_info.copy()
                t["timetable"] = schedule
                responseData[train_id].append(t)
            
           
           
            
            self.conn.publish(topic, json.dumps({
                    "stationFullname": self.get_full_stationname(station),
                    "schedule": [responseData]
                }))
      
   

    def filter(self, response, station):
        ''' filter by keys 
            (trainInfo, trainSchedule) '''
        rows = defaultdict(lambda: defaultdict(list))
        trains = dict()
        
        current_time = datetime.timestamp(datetime.now())
        
        for train in response: 
            filtered = ({key : train[key] for key in t_filter}, {} | {'destination': self.get_full_stationname(train['timeTableRows'][-1]['stationShortCode'])})
            
            train_type = train.get("commuterLineID", None) or train.get("trainType", "?")
             # TODO REDEFINE UGLY
            if train.get("commuterLineID", None):
                train_id = f'{train_type}'   
            else:
                train_id = f'{train.get("trainType", "?")}{train.get("trainNumber")}'
            ##
            
            transport_type = train.get('trainCategory')
            trains[train_id] = filtered[0]
            
            for i, row in enumerate(train['timeTableRows']):
                
                timestamp = datetime.strptime(row["scheduledTime"], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
                
                if row['stationShortCode'] == station:
                    for key in tt_filter:
                        filtered[1][key] = row.get(key, None)
                    
                    filtered[1]["stop_on_stations"] = [station['stationShortCode'] for station in train['timeTableRows'][i:] if station['trainStopping']][:5]
                        
                    
                    platform_id = row.get('commercialTrack', '?')
                    transit = row.get('type')
                    topic = f"station/{station}/{platform_id}/{transit}/{transport_type}"
                    
                    rows[topic][train_id].append(filtered[1])
                    
                    
        return trains, rows


    def aggregation(self):
        self.station_codes = rata.Simple('metadata/stations').get().onSuccess(lambda response, status, data : (
            response.json()
        )).send()
        
        
        
        self.trains = rata.Batch()
        for station in self.targets:
            self.trains.get(f'live-trains/station/{station}', payload={
                'minutes_before_departure': 120,
                'minutes_after_departure': 0,
                'minutes_before_arrival' : 10,
                'minutes_after_arrival': 0,
                'train_categories' : 'Commuter,Long-distance'
            }, onSuccess=lambda response, status, data, station=station : (
                filtered := self.filter(response.json(), station),
                self.pub(filtered, station)
            ))