import display_types as types
import mqtt_connection as mqtt
import argparse

# List contains all stations whose data is currently published
# This data can be obtained from the Management node e.g with MQTT topic "station/codes"
# OR just keep it hardcoded?
stationcodes = ["PSL", "HKI"]

parser = argparse.ArgumentParser(description='sets the correct display')
parser.add_argument('--s', type=str, help='enter station short code')
parser.add_argument('--t', type=str, help='enter platform number or "main" for main display')
args = parser.parse_args()


# Checks if user has set inputs with argparse
# If not it takes input from user
def initialize():
    if args.s is None and args.t is None:
        takeInput()
    else:
        args_station = args.s
        args_display_type = args.t
        if args_display_type == 'main':
            display = types.StationMainDisplay(args_station)
        else:
            display = types.PlatformDisplay(args_station, args_display_type)

        mqtt.createConnection([(display.getTopic(args_station), 1)], display)


def takeInput():
    print(f"Enter a station : {stationcodes} (case sensitive)")
    while True:
        station = input()
        if station not in stationcodes:
            print("Unvalid station code")
        else:
            break

    print("Choose a display type:\n1. Station main display \n2. Platform display \n3. Dual platform display")
    while True:
        try:
            display_type = int(input())
        except ValueError:
            print('Please enter an integer')
            continue
        if display_type == 1:
            display = types.StationMainDisplay(station)
            mqtt.createConnection([(display.getTopic(station), 1)], display)
            break
        elif display_type == 2:
            print("Enter platform number")
            platform = input()
            display = types.PlatformDisplay(station, platform)
            mqtt.createConnection([(display.getTopic(station), 1)], display)
            break
        elif display_type == 3:
            print("Enter left platform number")
            platform1 = input()
            print("Enter right platform number")
            platform2 = input()
            display = types.DualPlatformDisplay(station, platform1, platform2)
            mqtt.createConnection([(display.getTopic(station)[0], 1),
                                   (display.getTopic(station)[1], 1)], display)
            break
        else:
            print("Invalid input")


if __name__ == '__main__':
    initialize()
