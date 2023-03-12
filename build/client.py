import argparse
import display.display_types as types
from display import timetable_view, split_view
from display import mqtt_connection as mqtt


def main():
    parser = argparse.ArgumentParser(description='sets the correct display')
    parser.add_argument('-view', type=str, help='enter a display view name (tableview, splitview)')
    parser.add_argument('-s', type=str, help='enter station short code')
    parser.add_argument('-p', type=str, help='enter platform number')
    # parser.add_argument('--transit', type=str, help='enter transit type (departures, arrivals)')
    # parser.add_argument('--transport', type=str, help='enter transport type (commute, intercity, cargo)')
    parser.add_argument('-left', type=str, help='enter left display platform number')
    parser.add_argument('-right', type=str, help='enter right display platform number')
    args = parser.parse_args()

    if args.view == "splitview" and None not in [args.s, args.left, args.right]:
        display = types.DualPlatformDisplay(args.s, args.left, args.right)
        split_view.App()
        mqtt.createConnection(display)

    elif args.view == "tableview" and args.s is not None and args.p is None:
        display = types.TableCentralDisplay(args.s)
        # Setting column names and table row count
        timetable_view.App(["Time", "Notice", "Platform", "Train", "Destination"], 10)
        mqtt.createConnection(display)

    elif args.view == "tableview" and None not in [args.s, args.p]:
        display = types.TablePlatformDisplay(args.s, args.p)
        # Setting column names and table row count
        timetable_view.App(["Time", "Notice", "Train", "Destination"], 5)
        mqtt.createConnection(display)

    else:
        print("Invalid arguments")
        exit()


if __name__ == '__main__':
    main()
