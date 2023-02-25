import json
import requests

station_names = "https://rata.digitraffic.fi/api/v1/metadata/stations"

def get_station_names():
    #We fill variable "stationData" with info of stations from digitraffic
    response = requests.get(station_names)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print("Failed to get station names.")
        return None


#Helper function to return the full name of a station based on given shortCode
#"HPK" return "Haapamäki" for example
def get_station_name(short_code, station_data):
    if station_data != None:
        for station in station_data:
            if station['stationShortCode'] == short_code:
                return station['stationName']
    else:
        print("No station name for given shortCode")
        return None