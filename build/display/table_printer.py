import json
import os

from tabulate import tabulate

# Variables storing information for GUI
formatted = []
display_name = ''
warning_message = ''


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
    display_name = data["platform"]

    for x in data['trains']:
        if x['notice'] == '':
            formatted.append([x['time'], x['notice'], x['train'], x['destination']])
        else:
            formatted.append([x['time'], '-> ' + x['notice'], x['train'], x['destination']])
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
        if x['notice'] == '':
            formatted.append([x['time'], x['notice'], x['platform'], x['train'], x['destination']])
        else:
            formatted.append([x['time'], '-> ' + x['notice'], x['platform'], x['train'], x['destination']])
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'--------------{data["station"]}----------------')
    print(tabulate(formatted, headers=["Time", "Notice", "Platform", "Train", "Destination"]))
