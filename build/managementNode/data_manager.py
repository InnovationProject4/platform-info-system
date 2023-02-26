
import requests
import json
from datetime import datetime
import station_names as station_names

TIME = 600


#Helper to see what the index of trainstops(timeTablerows) is the departure from current station.
def check_index(data, station):

    #current time
    now = datetime.utcnow()

    #filter the timetableRows list for multiple entries of same station
    filtered_rows = [row for row in data if row.get("stationShortCode") == station and row.get("type") == "DEPARTURE"]

    #calculate the closer upcoming one for the given station
    differences = [abs(now - datetime.fromisoformat(row["scheduledTime"] [:-1])) for row in filtered_rows]

    #sort the rows and return the one wanted
    sorted_rows = [x for _,x in sorted(zip(differences, filtered_rows))]
    return data.index(sorted_rows[0])

##returns data of given station for next 10 hours (minutes_before_departure)
def get_data(station, stations):
    url = "https://rata.digitraffic.fi/api/v1/live-trains/station/" + station + "/?minutes_before_departure=" + str(TIME) + "&minutes_after_departure=0&minutes_before_arrival=0&minutes_after_arrival=0&train_categories=Commuter,Long-distance"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        trains = []
        current_time = datetime.utcnow()
       
        for x in data:
            train = x['trainNumber']
            stops = x['timeTableRows']
            end_station = stops[len(stops)-1]
            this_stop = stops[check_index(stops, station)]

            time = this_stop['scheduledTime']
            trainType = x['trainType']
            train_category = x['trainCategory']

            if 'actualTime' in this_stop:
                actual_time = this_stop['actualTime']
            else:
                actual_time = time
            notice = ""
            if 'differenceInMinutes' in this_stop:
                if 'differenceInMinute' in this_stop != 0:
                    notice = str(this_stop['differenceInMinutes'])

            platform = this_stop['commercialTrack']

            end_station_code = end_station['stationShortCode']
            destination = station_names.get_station_name(end_station_code, stations)   
            
            #Naming the trains (esim IC300 or "K" for "lähijunas")
            if (x['trainType'] == "HL"):
                commuter_id = x['commuterLineID']
                #check for kehärata trains
                if commuter_id == "P" or commuter_id == "I":
                    lentoasema = stops[check_index(stops, "LEN")]
                    helsinki = stops[check_index(stops, "HKI")]
                    if 'actualTime' in lentoasema:
                        t = lentoasema['actualTime']
                    else:
                        t = lentoasema['scheduledTime']
                    if 'actualTime' in helsinki:
                        t2 = helsinki['actualTime']
                    else:
                        t2 = helsinki['scheduledTime']
                    lentoasema_time = datetime.fromisoformat(t[:-1])
                    helsinki_time = datetime.fromisoformat(t[:-1])
                    if lentoasema_time < current_time and current_time > helsinki_time:
                        destination = "Helsinki asema"
                    else:
                        destination = "Lentoasema"

                    
            elif (x['trainType'] == "IC"):
                commuter_id = "IC" + str(x['trainNumber'])    
            elif (x['trainType'] == "S"):
                commuter_id = "S" + str(x['trainNumber']) 
            else:
                commuter_id = ""

            real_time = datetime.fromisoformat(actual_time[:-1])
            commercial_stop = this_stop['commercialStop']

            #if train hasn't Departured
            if real_time > current_time:
                if commercial_stop:
                    this_train = {'train': train, 'trainType': trainType, 'trainCategory': train_category, 'commuterID': commuter_id, 'time': time, 'actualTime': actual_time, 'notice': notice, 'platform': platform, 'destination': destination}
                    trains.append(this_train)
        return trains

        

def get_commercial_trains(data, amount):
    sorted_data = sorted(data, key=lambda x: x['time'])
    return sorted_data[:amount]

def get_track_data(data, track, amount):
    track_trains = []
    for train in data:
        if train['platform'] == str(track):
            track_trains.append(train)
    sorted_data = sorted(track_trains, key=lambda x: x['time'])
    return sorted_data[:amount]
