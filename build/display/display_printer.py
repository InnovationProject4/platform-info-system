import threading
import time
from datetime import datetime, timedelta
from utils.Event import Reactive
import json
import pytz
import utils.conf as conf
import utils.integrity as integrity
from utils.Tree import BPTree, query

# Reactive objects storing information for GUI
# which can update the GUI when the value changes
reactive_train_data = Reactive([])
reactive_train_data2 = Reactive([])  # Used to store splitviews left platform data
reactive_display_name = Reactive('')
reactive_warnings = Reactive([])
reactive_announcements = Reactive([])
reactive_passing = Reactive(False)
reactive_toast = Reactive("")

# Stores the time for the next passing train
passing_train_time = ''

# lists to store received messages
message_list = []
message_list2 = []

# Stores information from the display
topic_info_dict = {
    "station": "",
    "platform": "",
    "transit": "",
    "transport": "",
    "view": ""
}


def convertUTCtoEET(time):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    dt_utc = pytz.timezone("UTC").localize(datetime.strptime(time, date_format))
    dt_helsinki = dt_utc.astimezone(pytz.timezone("Europe/Helsinki"))
    return dt_helsinki.strftime('%H:%M')


# push a notification label on the display
def toast(message):
    reactive_toast.value = message


def verify(topic, message):
    '''Verify the integrity of data and extract the message, else return None'''
    res = integrity.verifyAndExtract(message.decode(), conf.Conf().cert)
    if res == None:
        '''message certifivate is invalid, toast orange message'''
        reactive_toast.value = ["A Message failed to pass integrity test", "warn"]
    return res


# Passing train check - function that the GUI checks every second
def checkPassingTrain():
    try:
        global passing_train_time, reactive_passing
        time_now = datetime.now(pytz.timezone("Europe/Helsinki"))
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        dt_utc = pytz.timezone("UTC").localize(datetime.strptime(passing_train_time, date_format))
        dt_helsinki = dt_utc.astimezone(pytz.timezone("Europe/Helsinki"))
        difference = dt_helsinki - time_now

        # Checks if passing train is one minute away from the station
        if dt_helsinki > time_now and dt_helsinki.date() == time_now.date() and (difference.seconds / 60) <= 1:
            print("Passing train incoming. Stay away from the platform")
            reactive_passing.value = True
        else:
            reactive_passing.value = False
    except ValueError:
        pass


def printPassingTrainOnDisplay(msg):
    try:
        parsed = json.loads(msg)
        if len(parsed['trains']) >= 1:
            global passing_train_time
            passing_train_time = parsed['trains'][0]['scheduledTime']
            print(passing_train_time)
    except Exception as e:
        print("Error decoding passing train JSON ", e)


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


# Function to handle received messages
# Loops through the trains to separate each train with only one timetable into new_trains list
# Sorts the list by scheduled time and "next_ten_trains"
def formatTrainData(trains, reactive_trains):
    global reactive_display_name
    topic_info_dict["station"] = trains[0]['stationFullname']

    t = BPTree(factor=50)

    for train in trains:
        print(len(train))
        popped = train.pop("schedule")
        t.bulk_insert(popped, lambda x: x['scheduledTime'])

    sorted = query.select_nodes(t.traverse, 10)

    formatted_train_data = []
    for train in sorted:
        temp_train_data = []
        temp_train_data.insert(3, train['commuterLineID'])
        temp_train_data.insert(4, train["destination"])
        temp_train_data.insert(5, train["stopOnStations"])
        temp_train_data.insert(0, convertUTCtoEET(train["scheduledTime"]))
        temp_train_data.insert(2, train['commercialTrack'])
        # Checks if train is late or cancelled
        if train["cancelled"] is False and train['differenceInMinutes'] == 0 or train['differenceInMinutes'] == "" or train['differenceInMinutes'] is None:
            temp_train_data.insert(1, "")
        elif train["cancelled"] is True:
            temp_train_data.insert(1, "Cancelled")
        else:
            if train['differenceInMinutes']:
                new_time = datetime.strptime(temp_train_data[0], '%H:%M') + timedelta(minutes=train['differenceInMinutes'])
                temp_train_data.insert(1, "→ " + new_time.strftime('%H:%M'))

        formatted_train_data.append(temp_train_data)

    configureDisplayName()
    reactive_trains.value = formatted_train_data


# Starts a thread to handle received messages.
# The reason for this function is that several consecutive messages can come from the same mqtt channel,
# for example if you subscribe with a wildcard subtopic.
# In this case, it must be ensured that all messages have been received before other operations.
def messageHandler(stop_event):
    global message_list, message_list2

    while not stop_event.is_set():
        # Waits for messages to arrive
        time.sleep(2)
        # Checks if any new messages have arrived in the last second
        last_message_time = time.time()
        while time.time() - last_message_time < 10 and len(message_list) == 0:
            time.sleep(1)
        # Collects messages received during the last 10 seconds into a list
        if len(message_list) != 0:
            messages = message_list
            message_list = []
            try:
                formatTrainData(messages, reactive_train_data)
            except Exception as e:
                print("Error formatting train data: ", e)
        if len(message_list2) != 0:
            messages = message_list2
            message_list2 = []
            try:
                formatTrainData(messages, reactive_train_data2)
            except Exception as e:
                print("Error formatting train data: ", e)


stop_event = threading.Event()
thread = threading.Thread(target=messageHandler, args=(stop_event,))
thread.start()


# Stops all running threads
def stop_threads():
    global stop_event, thread
    stop_event.set()
    thread.join(timeout=0.1)


def addTrains(msg, topic_dict):
    global message_list, topic_info_dict
    if topic_dict.get("station") is not None:
        topic_info_dict["station"] = topic_dict.get("station")
    if topic_dict.get("platform") is not None:
        topic_info_dict["platform"] = topic_dict.get("platform")
    if topic_dict.get("transit") is not None:
        topic_info_dict["transit"] = topic_dict.get("transit")
    if topic_dict.get("transport") is not None:
        topic_info_dict["transport"] = topic_dict.get("transport")
    if topic_dict.get("view") is not None:
        topic_info_dict["view"] = topic_dict.get("view")
    message_list.append(json.loads(msg))


# Second addTrains is used to listen to another topic for a display using "splitview"
def addTrains2(msg):
    global message_list2
    message_list2.append(json.loads(msg))


# Configures the text for the display_name_label in views
def configureDisplayName():
    global topic_info_dict, reactive_display_name
    name_dict = {
        "DEPARTURE": "departing ",
        "ARRIVAL": "arriving ",
        "Commuter": "commuter ",
        "Long-distance": "long distance ",
        "": ""
    }
    if topic_info_dict["view"] == "platformview":
        reactive_display_name.value = "Platform " + topic_info_dict["platform"]
        return
    if topic_info_dict["transit"] == "+" or topic_info_dict.get("transit") is None:
        topic_info_dict["transit"] = ""
    if topic_info_dict["transport"] == "#" or topic_info_dict.get("transport") is None:
        topic_info_dict["transport"] = ""
    if topic_info_dict["platform"] != "":
        reactive_display_name.value = "Platform " + topic_info_dict["platform"] + " " + name_dict[
            topic_info_dict['transit']] + name_dict[topic_info_dict['transport']] + "trains"
    else:
        reactive_display_name.value = topic_info_dict["station"] + " " + name_dict[topic_info_dict['transit']] + \
                                      name_dict[topic_info_dict['transport']] + "trains"
