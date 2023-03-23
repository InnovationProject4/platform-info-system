from tabulate import tabulate
from datetime import datetime
from utils.Event import Reactive
import json
import pytz
import os

# Variables storing information for GUI
reactive_train_data = Reactive([])
reactive_train_data2 = Reactive([])
reactive_display_name = Reactive('')
reactive_warnings = Reactive([])
reactive_announcements = Reactive([])
reactive_passing = Reactive(False)
passing_train_time = ''


def convertUTCtoEET(time):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    dt_utc = pytz.timezone("UTC").localize(datetime.strptime(time, date_format))
    dt_helsinki = dt_utc.astimezone(pytz.timezone("Europe/Helsinki"))
    return dt_helsinki.strftime('%H:%M')


def checkPassingTrain():
    try:
        global passing_train_time, reactive_passing
        time_now = datetime.now(pytz.timezone("Europe/Helsinki"))
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        dt_utc = pytz.timezone("UTC").localize(datetime.strptime(passing_train_time, date_format))
        dt_helsinki = dt_utc.astimezone(pytz.timezone("Europe/Helsinki"))
        difference = dt_helsinki - time_now

        # checks if passing train is one minute away from the station
        if dt_helsinki > time_now and dt_helsinki.date() == time_now.date() and (difference.seconds / 60) <= 1:
            print("Passing train incoming. Stay away from the platform")
            reactive_passing.value = True
        else:
            reactive_passing.value = False
    except ValueError:
        pass


def printPassingTrainOnDisplay(msg):
    parsed = json.loads(msg)
    if len(parsed['trains']) >= 1:
        global passing_train_time
        passing_train_time = parsed['trains'][0]['scheduledTime']
        print(passing_train_time)


def printAnnouncementsOnDisplay(msg):
    parsed = json.loads(msg)
    global reactive_announcements
    reactive_announcements.value = parsed
    # Color blue with ANSI code
    print(f"\033[34m{parsed} \033[00m")


def printWarningOnDisplay(msg):
    parsed = json.loads(msg)
    global reactive_warnings
    reactive_warnings.value = parsed
    # Color red with ANSI code
    print(f"\033[91m{parsed} \033[00m")


def printTablePlatformDisplay(msg):
    data = json.loads(msg)
    global reactive_train_data
    global reactive_display_name
    reactive_display_name.value = data['platform']
    temp_train_data = []

    for train in data['trains']:
        appendToTrainData(train, ['commuterID', 'destination'], temp_train_data)
    # using temp array so Reactive._notify doesnt trigger on every append
    reactive_train_data.value = temp_train_data
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'-----------------{data["platform"]}-------------------')
    print(tabulate(reactive_train_data.value, headers=["Time", "Notice", "Train", "Destination"]))


def printTableCentralDisplay(msg):
    data = json.loads(msg)
    global reactive_train_data
    global reactive_display_name
    reactive_display_name.value = data["station"]
    temp_train_data = []

    for train in data['trains']:
        appendToTrainData(train, ['platform', 'commuterID', 'destination'], temp_train_data)
    # using temp array so Reactive._notify doesnt trigger on every append
    reactive_train_data.value = temp_train_data
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'--------------{data["station"]}----------------')
    print(tabulate(reactive_train_data.value, headers=["Time", "Notice", "Platform", "Train", "Destination"]))


def printLeftDisplay(msg):
    data = json.loads(msg)
    global reactive_train_data
    reactive_train_data.value = printDualPlatformDisplay(data)
    print(f'--------------------Left-{data["platform"]}-----------------------')
    print(tabulate(reactive_train_data.value, headers=["Time", "Notice", "Platform", "Train", "Destination"]))


def printRightDisplay(msg):
    data = json.loads(msg)
    global reactive_train_data2
    reactive_train_data2.value = printDualPlatformDisplay(data)
    print(f'--------------------Right-{data["platform"]}-----------------------')
    print(tabulate(reactive_train_data2.value, headers=["Time", "Notice", "Platform", "Train", "Destination"]))


def printDualPlatformDisplay(t_data):
    train = t_data['trains'][0]
    temp = []
    appendToTrainData(train, ['platform', 'commuterID', 'destination'], temp)
    return temp


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
