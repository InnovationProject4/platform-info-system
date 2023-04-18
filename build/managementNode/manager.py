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
from managementNode import passing_train

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
            args = (info['uuid'], 0, info['display_name'], info['display_type'], dao.CONNECTED , data['messageTimestamp'], info['startTimestamp'])

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

    #Checks each train and makes dic of each topic to be published to. Publishes eachs topic.
    def publish(self, trains, station):
        train_dict = {}
        for train in trains:
            topic = train['topic']
            if topic not in train_dict:
                train_dict[topic] = []
            train_dict[topic].append(train)

        for topic, train_list in train_dict.items():
            sorted_train_list = sorted(train_list, key=lambda train: train['timetable']['scheduledTime'])
            self.conn.publish(topic, json.dumps({
                "stationFullname": self.get_full_stationname(station),
                "schedule": sorted_train_list
            }))

    def parse(self, response, station):

        #List of trains that we return in the end
        trains = []

        #iterate through trains in response and filter wanted info based on t_filter
        for train in response:
            filtered_train = ({key : train[key] for key in t_filter})
            filtered_train["destination"] = self.get_full_stationname(train["timeTableRows"][-1]["stationShortCode"])
            
            #List for filtered timetablerows of info of current stop to show
            filtered_timetablerows = []
            
            this_stop = None
            #Check for the wanted stop "this_stop" that matches station and hasn't passed yet.
            for i, row in enumerate(train['timeTableRows']):
                timestamp = (datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%S.%fZ") 
                this_time = None
                if row['stationShortCode'] == station:
                    if 'actualTime' in row and row['actualTime'] is not None and row['actualTime'] != '':
                        this_time = row['actualTime']
                    else:
                        this_time = row['scheduledTime']
                    if this_time >= timestamp:
                        this_stop = i
                        #checks next three stops for the train after this_stop
                        next_three = []
                        for r in train['timeTableRows'][this_stop+1:]:
                            if r.get('commercialStop') and r.get('type') == "ARRIVAL" :
                                if r.get('stationShortCode') != station:
                                    station_name = self.get_full_stationname(r.get('stationShortCode'))
                                    next_three.append(station_name)
                                    if len(next_three) >= 3:
                                        break
                        
                        #filter the row based on tt_filter and add it to the list of filtered timetablerows
                        filtered_row = {}
                        for key in tt_filter:
                            if key in row:
                                filtered_row[key] = row[key]
                            else:
                                filtered_row[key] = ""
                        filtered_row["stopOnStations"] = next_three
                        filtered_timetablerows.append(filtered_row)
                            
            filtered_train["timetable"] = filtered_timetablerows

            #each value in filtered_timetablerows represent a train
            #variable t represents train
            for i, timetablerow in enumerate(filtered_timetablerows):
                t = filtered_train.copy()
                t["timetable"] = timetablerow
                timestamp = t["timetable"]["scheduledTime"]

                #check kehäjuna and check if destination should be Airport(if it hasn't passed airport yet)
                for i, row in enumerate(train['timeTableRows']):
                    if row['stationShortCode'] == "LEN":
                        if row['scheduledTime'] > timestamp:
                            t["destination"] = self.get_full_stationname(row['stationShortCode'])
                t["timetable"]["destination"] = t["destination"]

                #Generate the topic based on the trains information and assign it as a value for key "topic"
                #append the trains list with train "t"
                platform_id = t["timetable"].get("commercialTrack", "")
                transit = t["timetable"].get("type", "")
                transport_type = t.get("trainCategory", "")
                trains.append({
                    **t,
                    "topic": f"station/{station}/{platform_id}/{transit}/{transport_type}"
                })

        #sorted_trains = sorted(trains, key=lambda x: x["timetable"]["scheduledTime"])
        #print(sorted_trains[:20])
        return trains
    


    def aggregation(self):
        self.station_codes = rata.Simple('metadata/stations').get().onSuccess(lambda response, status, data : (
            response.json()
        )).send()
        
        
        
        self.trains = rata.Batch()
        for station in self.targets:
            self.trains.get(f'live-trains/station/{station}', payload={
                'minutes_before_departure': 600,
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
