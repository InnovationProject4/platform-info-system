from tabulate import tabulate
from datetime import datetime
import json
import pytz
import os

# Variables storing information for GUI
train_data = []
train_data2 = []
display_name = ''
warning_message = ''
notification_message = ''
passing_train_time = ''


def convertUTCtoEET(time):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    dt_utc = pytz.timezone("UTC").localize(datetime.strptime(time, date_format))
    dt_helsinki = dt_utc.astimezone(pytz.timezone("Europe/Helsinki"))
    return dt_helsinki.strftime('%H:%M')


def checkPassingTrain():
    try:
        global passing_train_time
        time_now = datetime.now(pytz.timezone("Europe/Helsinki"))
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        dt_utc = pytz.timezone("UTC").localize(datetime.strptime(passing_train_time, date_format))
        dt_helsinki = dt_utc.astimezone(pytz.timezone("Europe/Helsinki"))
        difference = dt_helsinki - time_now

        # checks if passing train is one minute away from the station
        if dt_helsinki > time_now and dt_helsinki.date() == time_now.date() and (difference.seconds / 60) <= 1:
            print("Passing train incoming. Stay away from the platform")
            return True
        else:
            return False
    except ValueError:
        pass


def printPassingTrainOnDisplay(msg):
    parsed = json.loads(msg)
    if len(parsed['trains']) >= 1:
        global passing_train_time
        passing_train_time = parsed['trains'][0]['scheduledTime']
        print(passing_train_time)


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
    global train_data
    train_data = []
    global display_name
    display_name = data['platform']

    for train in data['trains']:
        appendToTrainData(train, ['commuterID', 'destination'], train_data)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'-----------------{data["platform"]}-------------------')
    print(tabulate(train_data, headers=["Time", "Notice", "Train", "Destination"]))


def printMainDisplay(msg):
    data = json.loads(msg)
    global train_data
    train_data = []
    global display_name
    display_name = data["station"]

    for train in data['trains']:
        appendToTrainData(train, ['platform', 'commuterID', 'destination'], train_data)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'--------------{data["station"]}----------------')
    print(tabulate(train_data, headers=["Time", "Notice", "Platform", "Train", "Destination"]))


def printLeftDisplay(msg):
    data = json.loads(msg)
    global train_data
    train_data = []
    printDualPlatformDisplay(data, train_data)
    print(f'--------------------Left-{data["platform"]}-----------------------')
    print(tabulate(train_data, headers=["Time", "Notice", "Platform", "Train", "Destination"]))


def printRightDisplay(msg):
    data = json.loads(msg)
    global train_data2
    train_data2 = []
    printDualPlatformDisplay(data, train_data2)
    print(f'--------------------Right-{data["platform"]}-----------------------')
    print(tabulate(train_data2, headers=["Time", "Notice", "Platform", "Train", "Destination"]))


def printDualPlatformDisplay(t_data, t_formatted):
    train = t_data['trains'][0]
    appendToTrainData(train, ['platform', 'commuterID', 'destination'], t_formatted)


def appendToTrainData(train, variables, formatted):
    if train['time'] == train['actualTime'] or train['actualTime'] == '':
        if train['notice'] == '':
            temp = [convertUTCtoEET(train['time']), train['notice']]
            for variable in variables:
                temp.extend([train[variable]])
            formatted.append(temp)
        else:
            temp = [convertUTCtoEET(train['time']), '~ ' + train['notice']]
            for variable in variables:
                temp.extend([train[variable]])
            formatted.append(temp)
    else:
        if train['notice'] == '':
            temp = [convertUTCtoEET(train['actualTime']), train['notice']]
            for variable in variables:
                temp.extend([train[variable]])
            formatted.append(temp)
        else:
            temp = [convertUTCtoEET(train['actualTime']), '~ ' + train['notice']]
            for variable in variables:
                temp.extend([train[variable]])
            formatted.append(temp)
