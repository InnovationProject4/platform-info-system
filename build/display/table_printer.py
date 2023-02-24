from tabulate import tabulate
from datetime import datetime
import json
import pytz
import os

# Variables storing information for GUI
formatted = []
display_name = ''
warning_message = ''
notification_message = ''


def convertUTCtoEET(time):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    dt_utc = pytz.timezone("UTC").localize(datetime.strptime(time, date_format))
    dt_helsinki = dt_utc.astimezone(pytz.timezone("Europe/Helsinki"))
    return dt_helsinki.strftime('%H:%M')


def printNotificationOnDisplay(msg):
    global notification_message
    notification_message = msg
    # Color blue with ANSI code
    print(f"\033[34m{msg} \033[00m")


def printWarningOnDisplay(msg):
    global warning_message
    warning_message = msg
    # Color red with ANSI code
    print(f"\033[91m{msg} \033[00m")


def printPlatformDisplay(msg):
    data = json.loads(msg)
    global formatted
    formatted = []
    global display_name
    display_name = data['trains'][0]['platform']

    for x in data['trains']:
        if x['time'] == x['actualTime'] or x['actualTime'] == '':
            if x['notice'] == '':
                formatted.append([convertUTCtoEET(x['time']), x['notice'], x['commuterID'], x['destination']])
            else:
                formatted.append([convertUTCtoEET(x['time']), '~ ' + str(x['notice']) + 'min', x['commuterID'], x['destination']])
        else:
            if x['notice'] == '':
                formatted.append([convertUTCtoEET(x['actualTime']), x['notice'], x['commuterID'], x['destination']])
            else:
                formatted.append([convertUTCtoEET(x['actualTime']), '~ ' + str(x['notice']) + 'min', x['commuterID'], x['destination']])
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'-----------------{data["platform"]}-------------------')
    print(tabulate(formatted, headers=["Time", "Notice", "Train", "Destination"]))


def printMainDisplay(msg):
    data = json.loads(msg)
    global formatted
    formatted = []
    global display_name
    display_name = data["station"]

    for x in data['trains']:
        if x['time'] == x['actualTime'] or x['actualTime'] == '':
            if x['notice'] == '':
                formatted.append([convertUTCtoEET(x['time']), x['notice'], x['platform'], x['commuterID'], x['destination']])
            else:
                formatted.append([convertUTCtoEET(x['time']), '~ ' + str(x['notice']) + 'min', x['platform'], x['commuterID'], x['destination']])
        else:
            if x['notice'] == '':
                formatted.append([convertUTCtoEET(x['actualTime']), x['notice'], x['platform'], x['commuterID'], x['destination']])
            else:
                formatted.append([convertUTCtoEET(x['actualTime']), '~ ' + str(x['notice']) + 'min', x['platform'], x['commuterID'], x['destination']])
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'--------------{data["station"]}----------------')
    print(tabulate(formatted, headers=["Time", "Notice", "Platform", "Train", "Destination"]))
