import argparse
import display_types as types
import mqtt_connection as mqtt
import timetable_view

parser = argparse.ArgumentParser(description='sets the correct display')
parser.add_argument('--s', type=str, help='enter station short code')
parser.add_argument('--p', type=str, help='enter platform number')
args = parser.parse_args()

args_station = args.s
args_platform = args.p
display = types.PlatformDisplay(args_station, args_platform)

column_labels = ["Time", "Notice", "Train", "Destination"]
rowcount = 5

timetable_view.App(column_labels, rowcount)

mqtt.createConnection(display.getTopic(args_station), display)
