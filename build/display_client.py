import argparse
import display.display_types as types
from display import timetable_view, split_view, platform_view, info_view
from display import mqtt_connection as mqtt


def main():
    parser = argparse.ArgumentParser(description='sets the correct display')
    parser.add_argument('-view', type=str, help='enter a display view name (tableview, splitview, platformview)')
    parser.add_argument('-s', type=str, help='enter station short code')
    parser.add_argument('-p', type=str, help='enter platform number')
    parser.add_argument('-transit', type=str, help='enter transit type (departures, arrivals)')
    parser.add_argument('-transport', type=str, help='enter transport type (commute, intercity, cargo)')
    parser.add_argument('-left', type=str, help='enter left display platform number')
    parser.add_argument('-right', type=str, help='enter right display platform number')
    args = parser.parse_args()

    conversion_dict = {
        "departures": "DEPARTURE",
        "arrivals": "ARRIVAL",
        "commute": "Long-distance",
        "intercity": "Commuter",
        "cargo": "Cargo"
    }

    args.transit = conversion_dict.get(args.transit, None)
    args.transport = conversion_dict.get(args.transport, None)

    if args.view == "splitview" and None not in [args.s, args.left, args.right, args.transit, args.transport]:
        display = types.DualPlatform(args.s, args.left, args.right, args.transit, args.transport)
        split_view.App()
        mqtt.createConnection(display, args.view)

    elif args.view == "tableview" and None not in [args.s, args.transit, args.transport] and args.p is None:
        display = types.Central(args.s, args.transit, args.transport)
        # Setting column names and table row count
        timetable_view.App(["Time", "Notice", "Platform", "Train", "Destination"], 10)
        mqtt.createConnection(display, args.view)

    elif args.view == "tableview" and None not in [args.s, args.p, args.transit, args.transport]:
        display = types.Platform(args.s, args.p, args.transit, args.transport)
        # Setting column names and table row count
        timetable_view.App(["Time", "Notice", "Train", "Destination"], 5)
        mqtt.createConnection(display, args.view)

    elif args.view == "platformview" and None not in [args.s, args.p, args.transit, args.transport]:
        display = types.Platform(args.s, args.p, args.transit, args.transport)
        # Setting column names and table row count
        platform_view.App()
        mqtt.createConnection(display, args.view)

    elif args.view == "infoview" and args.s is not None:
        display = types.Information(args.s)
        info_view.App()
        mqtt.createConnection(display, args.view)

    else:
        print("Invalid arguments")
        exit()


if __name__ == '__main__':
    main()
