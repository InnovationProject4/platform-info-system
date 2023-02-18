import json
import os

from tabulate import tabulate


def printPlatformDisplay(msg):
    data = json.loads(msg)
    formatted = []
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
    formatted = []
    for x in data['trains']:
        if x['notice'] == '':
            formatted.append([x['time'], x['notice'], x['platform'], x['train'], x['destination']])
        else:
            formatted.append([x['time'], '-> ' + x['notice'], x['platform'], x['train'], x['destination']])
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'--------------{data["station"]}----------------')
    print(tabulate(formatted, headers=["Time", "Notice", "Platform", "Train", "Destination"]))
