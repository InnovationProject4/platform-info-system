import json
import requests
import sys
import time
import paho.mqtt.client as paho

##List containing stations and their tracks that want data
listOfStations = [
    {
        'station': "HKI", 'tracks': ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10","11","12", "13" , "14", "15", "16", "17", "18", "19"]
    },
    {
        'station': "PSL", 'tracks': ["1", "2","3", "5", "8", "9", "10", "11"]
    },
    {
        'station': "HPL", 'tracks': ["1", "2", "3", "4"]
    },
]

client = paho.Client()

if client.connect("localhost", 1883, 60) != 0:
    print("error in connection")
    sys.exit(-1)

stationNames = "https://rata.digitraffic.fi/api/v1/metadata/stations"


#Helper to see what the index of trainstops(timeTablerows) is the departure from current station. haapamäki in this example
def checkIndex(data, station):
    i = 0
    for x in data:
        i+1
        if x['stationShortCode'] == station and x['type'] == "DEPARTURE":
            return i

#We fill variable "stationData" with info of stations from digitraffic
stationData = ""
stationsResponse = requests.get(stationNames)
if stationsResponse.status_code == 200:
    stationData = json.loads(stationsResponse.text)
else:
    stationData = None

#Helper function to return the full name of a station based on given shortCode
#"HPK" return "Haapamäki" for example
def getStationName(shortCode):
    if stationData!=None:
        for x in stationData:
            if x['stationShortCode'] == shortCode:
                return x['stationName']
    else:
        print("No data")
        return None

##Gives data from given url and sorts it according to time of departure
def sortedData(url):
    response = requests.get(url)
    

    if response.status_code == 200:
        data = json.loads(response.text)
        return data



##returns list of all departing passenger trains from given station and specified amount
##needed for mainDisplay information
def getAllDepartingTrains(stationCode, amount, data):
    
    trains = []
    for x in data:

        stops = x['timeTableRows']
        endStation = stops[len(stops)-1]
        thisStop = stops[checkIndex(stops, stationCode)]


        ## only takes info of tracks that we care (specified in listOfStations)
        checkStation = next((station for station in listOfStations if station['station'] == stationCode), None)        
        if checkStation is not None and str(thisStop['commercialTrack']) in checkStation['tracks']:

            train = str(x['trainNumber'])
            trainType = x['trainType']
            trainCategory = x['trainCategory']

            ##Time stuff
            time = thisStop['scheduledTime']
            if 'liveEstimateTime' in thisStop:
                actualTime = thisStop['liveEstimateTime']
            else:
                actualTime = time
            if 'differenceInMinutes' in thisStop:
                notice = thisStop['differenceInMinutes']
            else:
                notice = ""
            
            platform = str(thisStop['commercialTrack'])

            ##endstation stuff
            endStationCode = endStation['stationShortCode']
            destination = getStationName(endStationCode)

            trainStopping = str(thisStop['trainStopping'])
            commercialStop = str(thisStop['commercialStop'])

            ##check type of train for naming purpose  (esim: IC300 or "K")
            if (x['trainType'] == "HL"):
                commuterID = x['commuterLineID']
            elif (x['trainType'] == "IC"):
                commuterID = "IC" + str(x['trainNumber'])
            elif (x['trainType'] == "S"):
                commuterID = "S" + str(x['trainNumber'])
            else:
                commuterID = ''

            thisTrain = {'train': train, 'trainType': trainType, 'trainCategory': trainCategory, 'commuterID': commuterID, 'time': time, 'actualTime': actualTime, 'notice': notice, 'platform': platform, 'destination': destination, 'trainStopping': trainStopping, 'commercialStop': commercialStop}
            trains.append(thisTrain)

        ##sorting the trains
        def myFunc(e):
            return e['time']
        trains.sort(key=myFunc)

        thisStation = getStationName(stationCode)
        wantedData = {
            'station': thisStation,
            'trains': trains[0:10],
        }
        
    return wantedData

##Returns data of coming trains at 
def getTrackInfo(stationCode, wantedPlatform, data):
    trains = []
    for x in data:

        stops = x['timeTableRows']
        endStation = stops[len(stops)-1]
        thisStop = stops[checkIndex(stops, stationCode)]

        ## only takes info of tracks that we care (specified in listOfStations)
        checkStation = next((station for station in listOfStations if station['station'] == stationCode), None)        
        if checkStation is not None and str(thisStop['commercialTrack']) in checkStation['tracks']:
            train = str(x['trainNumber'])
            trainType = x['trainType']
            trainCategory = x['trainCategory']

            ##Time stuff
            time = thisStop['scheduledTime']
            if 'liveEstimateTime' in thisStop:
                actualTime = thisStop['liveEstimateTime']
            else:
                actualTime = time
            if 'differenceInMinutes' in thisStop:
                notice = thisStop['differenceInMinutes']
            else:
                notice = ""

            platform = thisStop['commercialTrack']

            ##endstation stuff
            endStationCode = endStation['stationShortCode']
            destination = getStationName(endStationCode)

            trainStopping = str(thisStop['trainStopping'])
            commercialStop = str(thisStop['commercialStop'])

            ##check type of train for naming purpose (esim: IC300 or "K")
            if (x['trainType'] == "HL"):
                commuterID = x['commuterLineID']
            elif (x['trainType'] == "IC"):
                commuterID = "IC" + str(x['trainNumber'])
            elif (x['trainType'] == "S"):
                commuterID = "S" + str(x['trainNumber'])
            else:
                commuterID = ''
            
            if str(platform) == wantedPlatform:
                
                thisTrain = {'train': train, 'trainType': trainType, 'trainCategory': trainCategory, 'commuterID': commuterID, 'time': time, 'actualTime': actualTime, 'notice': notice, 'platform': platform, 'destination': destination, 'trainStopping': trainStopping, 'commercialStop': commercialStop}
                trains.append(thisTrain)
    
    ##sorting the trains
    def myFunc(e):
        return e['time']
    trains.sort(key=myFunc)

    thisStation = getStationName(stationCode)
    wantedData = {
        'platform': platform,
        'trains': trains[0:5],
    }
    return wantedData





def makeRequest(topic, quality, station, track, data):
    if track == "main":
        data = getAllDepartingTrains(station, 10, data)
        client.publish(topic, json.dumps(data), quality)
    if track != "main":
        data = getTrackInfo(station, track, data)
        client.publish(topic, json.dumps(data), quality)




while True:
    for x in listOfStations:
        station = x['station']
        data = sortedData("https://rata.digitraffic.fi/api/v1/live-trains/station/" + station + "/?minutes_before_departure=720&minutes_after_departure=0&minutes_before_arrival=0&minutes_after_arrival=0&include_nonstopping=true")
        makeRequest("station/" + station + "/main", 0, station, "main", data)
        for z in x['tracks']:
            makeRequest("station/" + station + "/" + z, 0, station, z, data)
    print("Data published")
    time.sleep(20)