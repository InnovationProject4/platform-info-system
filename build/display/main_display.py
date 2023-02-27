import argparse
import display_types as types
import mqtt_connection as mqtt
import timetable_view

parser = argparse.ArgumentParser(description='sets the correct display')
parser.add_argument('--s', type=str, help='enter station short code')
args = parser.parse_args()

args_station = args.s
display = types.StationMainDisplay(args_station)

column_labels = ["Time", "Notice", "Platform", "Train", "Destination"]
rowcount = 10

timetable_view.App(column_labels, rowcount)

mqtt.createConnection(display.getTopic(args_station), display)
