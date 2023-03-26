import threading
import time

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







#TODO: Formatointi vanhaan muotoon & Destination = "Kovakoodattu stringi"
#####################################################################################################
#####################################################################################################
#####################################################################################################

# list to store received messages
message_list = []
message_list2 = []

# function to handle received messages
#Loops through the trains to separate each train with only one timetable into new_trains list
#sorts the list by scheduled time and "next_ten_trains"

def format_train_data(trains, reactive_trains):
    # sorts the train data
    new_trains = []
    for train in trains:
        for train_id, train_data in train.items():
            for timetable in train_data:
                for timetable_entry in timetable["timetable"]:
                    new_train = {
                        train_id: [{
                            "trainNumber": timetable["trainNumber"],
                            "trainType": timetable["trainType"],
                            "trainCategory": timetable["trainCategory"],
                            "commuterLineID": timetable["commuterLineID"],
                            "timetable": [timetable_entry]
                        }]
                    }
                    new_trains.append(new_train)

    sorted_trains = sorted(new_trains, key=lambda x: x[list(x.keys())[0]][0]['timetable'][0]['scheduledTime'])
    next_ten_trains = sorted_trains[:10]
    print("Handled messages \n", json.dumps(next_ten_trains), "\n\n")

    # final formatting for displays
    formatted = []
    for train in next_ten_trains:
        temp = []
        for train_data in train.values():
            temp.insert(3, train_data[0]['commuterLineID'])
            temp.insert(4, "puuttuu")
            for timetable in train_data[0]["timetable"]:
                if timetable["liveEstimateTime"] is None:
                    temp.insert(0, convertUTCtoEET(timetable["scheduledTime"]))
                else:
                    temp.insert(0, convertUTCtoEET(timetable["liveEstimateTime"]))
                temp.insert(2, timetable['commercialTrack'])
                if timetable["cancelled"] is False and timetable['differenceInMinutes'] == 0 or timetable['differenceInMinutes'] is None:
                    temp.insert(1, "")
                elif timetable["cancelled"] is True:
                    temp.insert(1, "Cancelled")
                else:
                    temp.insert(1, "~ " + str(timetable['differenceInMinutes']) + "min")

        formatted.append(temp)
    reactive_trains.value = formatted

    #return sorted_data[:amount]

    # do something with the messages, such as process or store them




# start a thread to handle received messages
def message_handler(stop_event):

    global message_list, message_list2

    while not stop_event.is_set():
        # wait for messages to arrive
        time.sleep(1)
        # check if any new messages have arrived in the last second
        last_message_time = time.time()
        while time.time() - last_message_time < 10 and len(message_list) == 0:
            time.sleep(1)
        # collect messages received during the last 10 seconds into a list
        if len(message_list) != 0:
            messages = message_list
            message_list = []
            format_train_data(messages, reactive_train_data)
        if len(message_list2) != 0:
            messages = message_list2
            message_list2 = []
            format_train_data(messages, reactive_train_data2)



stop_event = threading.Event()
thread = threading.Thread(target=message_handler, args=(stop_event,))
thread.start()

def stop_threads():
    # Stop all running threads
    global stop_event
    global thread

    stop_event.set()
    thread.join()


def addTrains(msg, display_name):
    global message_list, reactive_display_name
    message_list.append(json.loads(msg))
    reactive_display_name.value = display_name


def addTrains2(msg):
    global message_list2
    message_list2.append(json.loads(msg))


   #####################################################################################################
   #####################################################################################################
   #####################################################################################################


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
