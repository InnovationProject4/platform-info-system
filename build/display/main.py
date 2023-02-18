import display_types as types
import mqtt_connection as mqtt

# List contains all stations whose data is currently published
# This data can be obtained from the Management node e.g with MQTT topic "station/codes"
# OR just keep it hardcoded?
stationcodes = ["PSL", "HKI"]


def initializeDisplay():
    print(f"Enter a station : {stationcodes} (case sensitive)")
    while True:
        station = input()
        if station not in stationcodes:
            print("Unvalid station code")
        else:
            break

    print("Choose a display type:\n1. Station main display \n2. Platform display")
    while True:
        try:
            display_type = int(input())
        except ValueError:
            print('Please enter an integer')
            continue
        if display_type == 1:
            display = types.StationMainDisplay()
            break
        elif display_type == 2:
            print("Enter platform number")
            platform = input()
            display = types.PlatformDisplay(platform)
            break
        else:
            print("Invalid input")

    mqtt.createConnection(display.getTopic(station), display)


if __name__ == '__main__':
    initializeDisplay()

