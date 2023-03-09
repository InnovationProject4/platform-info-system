import argparse
from tkinter import *
import threading
import table_printer as tp
from datetime import datetime
import gui_helper
import display_types as types
import mqtt_connection as mqtt

parser = argparse.ArgumentParser(description='sets the correct display')
parser.add_argument('--s', type=str, help='enter station short code')
parser.add_argument('--left', type=str, help='enter platform number')
parser.add_argument('--right', type=str, help='enter platform number')
args = parser.parse_args()

args_station = args.s
args_platform1 = args.left
args_platform2 = args.right
display = types.DualPlatformDisplay(args_station, args_platform1, args_platform2)


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
        self.root['bg'] = '#0a4a70'
        self.root.geometry("640x360")
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 1, weight=7)

        top_frame = Frame(self.root, bg='#031626')
        Grid.columnconfigure(top_frame, 0, weight=1)
        Grid.columnconfigure(top_frame, 1, weight=1)

        Grid.rowconfigure(top_frame, 0, weight=1)
        display_name_label = Label(top_frame, text="", fg='white', bg='#031626', font=('Calibri Light', 25))
        display_name_label.grid(row=0, column=0, sticky="W", padx=(20, 0))

        time_label = Label(top_frame, text="", fg='white', bg='#031626', font=('Calibri Light', 15))
        time_label.grid(row=0, column=1, sticky="E", padx=(0, 20))

        main_frame = Frame(self.root, bg='#061f36')
        Grid.columnconfigure(main_frame, 0, weight=2)
        Grid.columnconfigure(main_frame, 1, weight=1)
        Grid.columnconfigure(main_frame, 2, weight=2)

        arrive_label = Label(main_frame, text="1 Min", fg='white', anchor='e', justify=RIGHT, bg='#061f36',
                             font=('Calibri Light', 15))
        arrive_label.grid(row=0, column=0, sticky="SEW")

        destination_label = Label(main_frame, text="Leppävaara", anchor='e', justify=RIGHT, fg='white', bg='#061f36',
                                  font=('Calibri Light', 30))
        destination_label.grid(row=1, column=0, sticky="NSEW")

        platform_label = Label(main_frame, text="4", anchor='e', justify=RIGHT, fg='white', bg='#061f36',
                               font=('Calibri Light', 35))
        platform_label.grid(row=0, column=2, sticky="NSEW", padx=(0, 100))

        stops_label = Label(main_frame, text="Alberga\nGöckerbacka\nMatinkylä\nHuopalahti", fg='white', bg='#061f36',
                            anchor='w', justify=LEFT, font=('Calibri Light', 15))
        stops_label.grid(row=1, column=2, rowspan=9, sticky="NSEW")

        notification_label = Label(self.root, text="", fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        notification_label.grid(row=2, column=0, sticky="NSEW", pady=(0, 7))

        warning_frame = Frame(self.root, bg='#0a4a70')
        warning_label = Label(warning_frame, text="", fg='red', bg='#0a4a70', font=('Calibri Light', 15))
        warning_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        def configureLabels(data, l):
            i = 0
            for label in l:
                try:
                    if (i + 1) == 1 and data[0][1] != "":
                        label['text'] = data[0][0] + data[0][1]
                        i += 1
                    elif i == 0:
                        label['text'] = data[0][i]
                        i += 1
                    else:
                        label['text'] = data[0][i]
                    i += 1
                except IndexError:
                    label['text'] = ''

        def update():
            # data1 = tp.formatted
            # data2 = tp.formatted2
            display_name_label['text'] = tp.display_name
            warning_label['text'] = tp.warning_message
            if tp.warning_message != '':
                warning_frame.tkraise()
            else:
                main_frame.tkraise()
            notification_label['text'] = tp.notification_message
            time_label['text'] = datetime.now().strftime("%H:%M:%S")

            # configureLabels(data1, left_labels)
            # configureLabels(data2, right_labels)

            checkResize()
            self.root.after(1000, update)

        def checkResize():
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            if w > 1500 and h > 500:
                resizeFonts(40, 40, 40, 35, 30, 95, 50)
                return
            elif w > 1000 and h > 500:
                resizeFonts(35, 35, 35, 25, 25, 75, 40)
                return
            elif w > 600 and h > 400:
                resizeFonts(25, 25, 25, 15, 20, 65, 35)
                return
            elif w > 300 and h > 200:
                resizeFonts(15, 15, 15, 10, 15, 40, 20)
                return

        def resizeFonts(s_name, s_warning, s_time, s_notification, s_stops, s_platform, s_arrive):
            display_name_label['font'] = ('Calibri Light', s_name)
            notification_label['font'] = ('Calibri Light', s_notification)
            warning_label['font'] = ('Calibri Light', s_warning)
            time_label['font'] = ('Calibri Light', s_time)
            arrive_label['font'] = ('Calibri Light', s_arrive)
            destination_label['font'] = ('Calibri Light', s_platform)
            platform_label['font'] = ('Calibri Light', s_platform)
            stops_label['font'] = ('Calibri Light', s_stops)

        top_frame.grid(row=0, column=0, sticky="NSEW")
        warning_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.tkraise()

        update()
        self.root.mainloop()


App()
