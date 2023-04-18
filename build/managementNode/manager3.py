import json
from datetime import datetime
import utils.conf as conf
import utils.integrity as integrity
import messaging.ratatraffic as rata
from messaging.telemetry import Connection 
from utils.database.sqlite import PersistentConnection
import utils.database.model.display as dao
from collections import defaultdict
from managementNode import announcement_manager
from utils.Event import observable
from utils.Tree import BPTree, query
from managementNode import passing_train

dbconnection = PersistentConnection()

# select the railway stations to filter for using shortStationCodes
targets = []

class Manager:
    def __init__(self, stations=[]):
        self.conn = Connection(conf.ADDR, conf.PORT)
        self.conn.client.on_connect = self.on_connect
        
        # data integrity tokens
        self.cert, self.pkey = integrity.load(conf.ENC_PATH, conf.TOKEN)
        
        self.targets = stations
        
        self.aggregation()
        self.conn.connect()

    def on_connect(self, client, userdata, flags, rc):
        self.conn.on_connect(client, userdata, flags, rc)

        self.conn.subscribe_multiple([
            
            ("management", lambda client, userdata, message : (
                payload := json.loads(message.payload.decode('utf-8')),
                print("A device handshake from ", payload['event']),
                self.register_display(payload) if payload['event'] == 'startup' else self.shutdown_signal(payload) if payload['event'] == 'shutdown' else None
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
        """Get the display information from the database."""
        with PersistentConnection() as (conn, cur):
            display = dao.Display(conn=conn)
            display.schema()
            
            dinfo = display.fetchall()
            if dinfo:
                return dinfo

            return dinfo
        
        
    def get_full_stationname(self, code):
        stationname = self.station_codes.get(code, None)
        if stationname is None:
            print("No such station code in the dictionary.")
            return code
        else:
            return stationname



    def shutdown_signal():
        '''   Display notified that it is shutting down and no longer active. '''
        

    @observable
    def register_display(self, data):
        '''
            when manager receives "startup" event, it attempts to save the information from the display and send back 'ack' event message (Acknowledged).
            Startup event message comes with display's unique public key and during acknowledgement, the manager sends back it's own public key to the display,
            which will be used to verify all the following messages.
        '''
        with PersistentConnection() as (conn, cur):
            display = dao.Display(conn=conn)
            display.schema()

            info = data['message']
            args = (info['uuid'], 0, info['display_name'], info['display_type'], dao.CONNECTED , data['messageTimestamp'], info['startTimestamp'])

            display.insert(*args)
            
            if cur.rowcount == 0:
                 display.update(*args)
            else:
                # confirm registraction and send certificate
                print("acknowledged display: ", info['uuid'])
                self.conn.publish(f"management/{info['uuid']}", json.dumps({
                    "event": "ack",
                    "messageTimestamp": datetime.timestamp(datetime.now()),
                    "message": integrity.dump_certificate(integrity.FILETYPE_PEM, self.cert).decode()
                }))
                
    
    
    def publish(self, trains, station):
        """Publish the train schedule to the broker.
        
        Args:   
            tables (list): The list of filtered train data tables in order of topic
            station (str): The station to filter for in topic parsing.
        """
        
        current_timestamp = (datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%S.%fZ") 
        full_station_name = self.get_full_stationname(station)
            
        for topic, data in trains.items():
            
            payload = integrity.signMessage(json.dumps({
                "messageTimestamp": current_timestamp,
                "stationFullname": full_station_name,
                "schedule": data
            }), self.pkey)
            
            self.conn.publish(topic, payload)
   

    def parse(self, response, station):
        """Parse the response from the API and return a list of trains.
        
        Args:
            response (list): The response from the API.
            station (str): The station to filter for.
            
        Returns:
            list: The list of tables (BPTrees) in order, topic rows, trainData rows, train Schedule rows.
        """
        timestamp = (datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        
        # B+ Tree to sort and query base train info and train timetables
        trains = BPTree(factor=50)
        schedules = BPTree(factor=50)
        
        #topics are more straigh forward, so we use a dict
        topics = defaultdict(list)
        

        for train in response:
            ## initial parsing of the train data
            
            if train["trainType"] != "HL":
               train["commuterLineID"] = train["trainType"] + str(train["trainNumber"])
               
            timetables = train.pop('timeTableRows')
            
            # insert basic train info into a BP Tree
            trains.insert(train['trainNumber'], train)
        
            # insert train schedule timetables and add destination, train_id as foreign key and id as unique key, using scheduledTime as primary key
            schedules.bulk_insert(timetables, lambda x, t=train: (
                cid := id((x['scheduledTime'], x['type'], t['trainNumber'])),
                x.update({
                    "id": cid,
                    "train_id": t["trainNumber"], 
                    "destination": self.get_full_stationname(timetables[-1]['stationShortCode']) }),
              
                x["scheduledTime"]
            )[-1])
            
            
        ## Get all timetables for current station and insert to topic_rows with the data
        
        # select the desired columns from the 'timeTableRows' list
        # ex. 'train_id', 'type', 'cancelled', 'scheduledTime', 'differenceInMinutes', 'liveEstimateTime', 'actualTime', 'commercialTrack', 'trainStopping', 'cause', 'destination', 'stop_on_stations'
        # on base train data that would be:
        # ex. train_data = 'trainNumber', 'trainType', 'trainCategory', 'commuterLineID'
        for s in query.select(schedules.range_query(timestamp, "9999999099"), 
                                    'id', 
                                    'train_id', 
                                    'type', 
                                    'cancelled', 
                                    'scheduledTime', 
                                    'differenceInMinutes', 
                                    'liveEstimateTime', 
                                    'actualTime', 
                                    'commercialTrack', 
                                    'trainStopping', 
                                    'cause',
                                    'destination',
                                    
                                    stationShortCode=station, scheduledTime = lambda x : x >= timestamp):
            
            trainNumber = s['train_id']
            
            next_stops = []
            # get next stops for the train after current station
            for stop in query.select(schedules.range_query(s['scheduledTime'], "9999999999"), 'stationShortCode', 
                                    trainNumber=trainNumber,
                                    commercialStop=True, 
                                    type="ARRIVAL", 
                                    stationShortCode= lambda x: x != station, 
                                    scheduledTime= lambda x : x > s['scheduledTime']):
                
                next_stops.append(self.get_full_stationname(stop['stationShortCode']))
                
            s['stopOnStations'] = next_stops
                
                
            # Some trains have special destination labels in HSL
            #check kehäjuna and check if destination should be LEN (if it hasn't passed airport yet)
            LEN = query.select(schedules.traverse(), "stationShortCode", stationShortCode="LEN", type="ARRIVAL", trainNumber=trainNumber, scheduledTime= lambda x : x > s['scheduledTime'])
            
            if len(LEN) > 0: 
                s['destination'] = self.get_full_stationname("LEN")
                
                
            # inner join with train table 
            s['commuterLineID'] = trains.find(trainNumber).get("commuterLineID", "")
            s['trainCategory'] = trains.find(trainNumber).get("trainCategory", "")
                
            
            # insert timetable id as reference foreign key, into topic_rows table with topic as key
            platform_id = s.get("commercialTrack", "")
            transit = s.get("type", "")
            transport_type = trains.find(trainNumber).get("trainCategory", "")
            
            t = f'station/{station}/{platform_id}/{transit}/{transport_type}'
            topics[t].append(s)

            
        return topics
                
    
    def aggregation(self):
        ''' Short to full station naming '''
        self.station_codes = rata.Simple('metadata/stations').get().onSuccess(lambda response, status, data : (
            {s["stationShortCode"]: s["stationName"] for s in response.json()}
        )).send()
        
        
        ''' Causes of train delays '''
        self.causes = rata.Simple('metadata/detailed-cause-category-codes').get().onSuccess(lambda response, status, data : (
            {s["detailedCategoryCode"]: s for s in response.json()}
        ))
        
        
        
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
       
            
    def publish_passing_train_data(self, station):
        topic = f"station/{station}/passing"
        passing_train_data = passing_train.get_passing_train(station)

        if passing_train_data:
            formatted_data = {
                "station": station,
                "trains": passing_train_data
            }
            self.conn.publish(topic, json.dumps(formatted_data), 0)
            