from tkinter import *
import threading
import display_types as types
import mqtt_connection as mqtt
import gui_helper
import argparse
import table_printer as tp

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

        self.root.geometry("500x500")
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 1, weight=7)

        top_frame = Frame(self.root, bg='#0a4a70')

        Grid.rowconfigure(top_frame, 0, weight=1)
        Label(top_frame, text="Pasila Station", fg='white', bg='#0a4a70', font=('Consolas', 25)).grid(row=0, column=0,
                                                                                                      sticky="NSEW")

        main_frame = Frame(self.root, bg='#0a4a70')
        Label(self.root, text="Warning message?", fg='red', bg='#0a4a70', font=('Consolas', 15)).grid(row=2, column=0,
                                                                                             sticky="NSEW")

        print(display.getType())
        gui_helper.configureGrid(display.getType(), main_frame, Grid)

        labels = gui_helper.fillGrid(display.getType(), main_frame)

        def update():
            data = tp.formatted
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

            self.root.after(1000, update)

        top_frame.grid(row=0, column=0, sticky="NSEW")
        main_frame.grid(row=1, column=0, sticky="NSEW")

        update()

        self.root.mainloop()


app = App()

mqtt.createConnection(display.getTopic(args_station), display)
