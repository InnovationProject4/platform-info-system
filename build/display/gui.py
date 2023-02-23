from tkinter import *
import threading
import display_types as types
import mqtt_connection as mqtt
import gui_helper
import argparse
import table_printer as tp
from datetime import datetime

parser = argparse.ArgumentParser(description='sets the correct display')
parser.add_argument('--s', type=str, help='enter station short code')
parser.add_argument('--t', type=str, help='enter platform number or "main" for main display')
args = parser.parse_args()

args_station = args.s
args_display_type = args.t
if args_display_type == 'main':
    display = types.StationMainDisplay(args_station)
else:
    display = types.PlatformDisplay(args_station, args_display_type)


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.root = None
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root['bg'] ='#0a4a70'
        self.root.geometry("640x360")
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 1, weight=7)

        top_frame = Frame(self.root, bg='#0a4a70')
        Grid.columnconfigure(top_frame, 0, weight=1)
        Grid.columnconfigure(top_frame, 1, weight=1)

        Grid.rowconfigure(top_frame, 0, weight=1)
        display_name_label = Label(top_frame, text="", fg='white', bg='#0a4a70', font=('Calibri Light', 25))
        display_name_label.grid(row=0, column=0, sticky="W", padx=(20, 0))

        time_label = Label(top_frame, text="", fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        time_label.grid(row=0, column=1, sticky="E", padx=(0, 20))

        main_frame = Frame(self.root, bg='#0a4a70')

        warning_label = Label(self.root, text="", fg='red', bg='#0a4a70', font=('Calibri Light', 15))
        warning_label.grid(row=2, column=0, sticky="NSEW", pady=(0, 7))

        gui_helper.configureGrid(display.getType(), main_frame, Grid)

        labels = gui_helper.fillGrid(display.getType(), main_frame)

        def update():
            data = tp.formatted
            display_name_label['text'] = tp.display_name
            warning_label['text'] = tp.warning_message
            time_label['text'] = datetime.now().strftime("%H:%M:%S")
            train = 0
            info = 0
            for label in labels:
                try:
                    label['text'] = data[train][info]
                    info += 1
                    if info == len(data[train]):
                        info = 0
                        train += 1
                except IndexError:
                    label['text'] = ''
            checkResize()
            self.root.after(1000, update)

        def checkResize():
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            if w > 1500 and h > 500:
                resizeFonts(40, 40, 40, 35)
                return
            elif w > 1000 and h > 500:
                resizeFonts(35, 35, 35, 25)
                return
            elif w > 600 and h > 400:
                resizeFonts(25, 25, 25, 15)
                return
            elif w > 300 and h > 200:
                resizeFonts(15, 15, 15, 10)
                return

        def resizeFonts(s_name, s_warning, s_time, s_trains):
            display_name_label['font'] = ('Calibri Light', s_name)
            warning_label['font'] = ('Calibri Light', s_warning)
            time_label['font'] = ('Calibri Light', s_time)
            for label in labels:
                label['font'] = ('Calibri Light', s_trains)

        top_frame.grid(row=0, column=0, sticky="NSEW")
        main_frame.grid(row=1, column=0, sticky="NSEW")

        update()

        self.root.mainloop()


app = App()

mqtt.createConnection(display.getTopic(args_station), display)
