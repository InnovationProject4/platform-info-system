import json
from datetime import datetime, timedelta
import messaging.ratatraffic as rata
from messaging.telemetry import Connection 
from utils.database.sqlite import PersistentConnection
import utils.database.model.display as dao
import configparser
from collections import defaultdict
from managementNode import announcement_manager
from utils.Event import observable
from utils.Tree import BPTree

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
        


    @observable
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
                
    
    
    def publish(self, rows, station):
        trains_baseinfo, schedules = rows
        
        for topic, trains in schedules.items():
            responseData = defaultdict(list)
             
            for train_id, schedule in trains.items():
                train_info = trains_baseinfo[train_id]
                    
                t = train_info.copy()
                t["timetable"] = schedule
                responseData[train_id].append(t)
            
            print(json.dumps({
                        "stationFullname": self.get_full_stationname(station),
                        "schedule": [responseData]
                    }))
            
                
            
            self.conn.publish(topic, json.dumps({
                    "stationFullname": self.get_full_stationname(station),
                    "schedule": [responseData]
                }))
      
   

    def parse(self, response, station):
        ''' filter by keys 
            (trainInfo, trainSchedule) '''
        rows = defaultdict(lambda: defaultdict(list))
        trains = dict()
        timestamp = (datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%S.%fZ") 
        
        # B+ Tree to sort and query base train info and train timetables
        trains = BPTree(factor=50)
        schedules = BPTree(factor=50)
        
        # iterate through base train information and adjust
        for train in response:
            if train["trainType"] != "HL":
               train["commuterLineID"] = train["trainType"] + str(train["trainNumber"])
            
            # iterate through train schedule timetables and parse according to our needs
            this_stop = None
            for i, row in enumerate(train["timeTableRows"]):
                if row['stationShortCode'] == station:
                    
                    # use actualTime if exists, otherwise use scheduledTime
                    row['actualTime'] = row.get("actualTime", row["scheduledTime"])
                    
                    if row['actualTime'] >= timestamp:
                        this_stop = i
                        
                        
                        #checks next five stops for the train after this_stop
                        next_stops = []
                        for r in train['timeTableRows'][this_stop+1:]:
                             if r.get('commercialStop') and r.get('type') == "ARRIVAL" :
                                 stationShortCode = r.get('stationShortCode')
                                 if stationShortCode != station:
                                     next_stops.append(self.get_full_stationname(stationShortCode))
                                     if len(next_stops) >= 5:
                                         break
                                     
                        
                        # Some trains have special destination labels in HSL
                        #check kehäjuna and check if destination should be Airport(if it hasn't passed airport yet)
                        
                                     
                                     
                    
                        row["stop_on_stations"] = next_stops
                        row["id"] = train["commuterLineID"]
                        row["destination"] = self.get_full_stationname(train['timeTableRows'][-1]['stationShortCode'])
                        
                        
                        schedules.insert(row['actualTime'], row)
                        
                            
                    
                    
                    
                    
                    
                
                
                
                
                
               
            
            
      
            
            
                    
                    
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
                filtered := self.parse(response.json(), station),
                self.publish(filtered, station)
            ))