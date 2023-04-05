import argparse
import display.display_types as types
from display import timetable_view, split_view, platform_view, info_view
from display import mqtt_connection as mqtt, display_printer as dp


def main():
    parser = argparse.ArgumentParser(description='sets the correct display')
    parser.add_argument('-view', type=str, help='enter a display view name (tableview, splitview, platformview, infoview)')
    parser.add_argument('-s', type=str, help='enter station short code')
    parser.add_argument('-p', type=str, help='enter platform number')
    parser.add_argument('-transit', type=str, help='enter transit type (departures, arrivals)')
    parser.add_argument('-transport', type=str, help='enter transport type (commuter, long_distance)')
    parser.add_argument('-left', type=str, help='enter left display platform number')
    parser.add_argument('-right', type=str, help='enter right display platform number')
    args = parser.parse_args()

    # Converting the arguments to the actual naming used in the topic
    conversion_dict = {
        "departures": "DEPARTURE",
        "arrivals": "ARRIVAL",
        "commuter": "Commuter",
        "long_distance": "Long-distance"
    }

    # Subscribes to all subtopics if argument is left out
    args.transit = conversion_dict.get(args.transit, "+")
    args.transport = conversion_dict.get(args.transport, "#")

    # 1. Checks if the correct arguments are given
    # 2. Creates a display object that defines the necessary topics
    # 3. Starts the GUI
    # 4. Creates an MQTT connection based on the topics of the display object
    if args.view == "splitview" and None not in [args.s, args.left, args.right, args.transit, args.transport]:
        display = types.DualPlatform(args.s, args.left, args.right, args.transit, args.transport)
        split_view.App()
        mqtt.createConnection(display, args.view)

    elif args.view == "tableview" and None not in [args.s, args.transit, args.transport] and args.p is None:
        display = types.Central(args.s, args.transit, args.transport)
        # Setting column names and table row count
        timetable_view.App(["Time", "Notice", "Train", "Platform", "Destination"], 10)
        mqtt.createConnection(display, args.view)

    elif args.view == "tableview" and None not in [args.s, args.p, args.transit, args.transport]:
        display = types.Platform(args.s, args.p, args.transit, args.transport, "tableview")
        # Setting column names and table row count
        timetable_view.App(["Time", "Notice", "Train", "Destination"], 5)
        mqtt.createConnection(display, args.view)

    elif args.view == "platformview" and None not in [args.s, args.p, args.transit, args.transport]:
        display = types.Platform(args.s, args.p, args.transit, args.transport, "platformview")
        platform_view.App()
        mqtt.createConnection(display, args.view)

    elif args.view == "infoview" and args.s is not None:
        display = types.Information(args.s)
        info_view.App()
        mqtt.createConnection(display, args.view)

    else:
        print("Invalid arguments")
        dp.stop_threads()
        exit()


if __name__ == '__main__':
    main()
