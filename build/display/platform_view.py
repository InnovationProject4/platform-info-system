import configparser
from tkinter import *
import threading
from display import gui_helper, display_printer as dp, mqtt_connection as mqtt
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')
full_screen = config.get('display', 'fullscreen')


class App(threading.Thread):

    def __init__(self, announcement_id=0, warning_id=0):
        self.announcement_id = announcement_id
        self.warning_id = warning_id
        threading.Thread.__init__(self)
        self.root = None
        self.start()

    def callback(self):
        self.root.quit()

    def onClose(self):
        mqtt.onDisconnect()
        dp.stop_threads()
        self.callback()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.root['bg'] = '#0a4a70'
        self.root.geometry("640x360")
        self.root.attributes('-fullscreen', full_screen)
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 1, weight=7)

        top_frame = Frame(self.root, bg='#031626')
        main_frame = Frame(self.root, bg='#061f36')
        warning_frame = Frame(self.root, bg='#0a4a70')

        Grid.columnconfigure(top_frame, 0, weight=1)
        Grid.columnconfigure(top_frame, 1, weight=1)
        Grid.rowconfigure(top_frame, 0, weight=1)

        display_name_label = Label(top_frame, text="", fg='white', bg='#031626', font=('Calibri Light', 25))
        display_name_label.grid(row=0, column=0, sticky="W", padx=(20, 0))
        dp.reactive_display_name.watch(lambda: gui_helper.updateLabels(dp.reactive_display_name.value, display_name_label))

        time_label = Label(top_frame, text="", fg='white', bg='#031626', font=('Calibri Light', 15))
        time_label.grid(row=0, column=1, sticky="E", padx=(0, 20))

        Grid.columnconfigure(main_frame, 0, weight=1)
        Grid.columnconfigure(main_frame, 1, weight=1)
        Grid.columnconfigure(main_frame, 2, weight=2)
        Grid.rowconfigure(main_frame, 0, weight=1)
        Grid.rowconfigure(main_frame, 1, weight=1)
        Grid.rowconfigure(main_frame, 2, weight=6)

        arrive_label = Label(main_frame, text="", fg='white', anchor='e', justify=RIGHT, bg='#061f36', font=('Calibri Light', 15))
        arrive_label.grid(row=0, column=0, sticky="SEW")
        dp.reactive_train_data.watch(lambda: gui_helper.updateLabels(f"{dp.reactive_train_data.value[0][0]} {dp.reactive_train_data.value[0][1]}", arrive_label))

        destination_label = Label(main_frame, text="", anchor='e', justify=RIGHT, fg='white', bg='#061f36', font=('Calibri Light', 30))
        destination_label.grid(row=1, column=0, sticky="NSEW")
        dp.reactive_train_data.watch(lambda: gui_helper.updateLabels(dp.reactive_train_data.value[0][4], destination_label))

        train_label = Label(main_frame, text="", anchor='e', justify=RIGHT, fg='white', bg='#061f36', font=('Calibri Light', 35))
        train_label.grid(row=0, column=2, sticky="NSEW", padx=(0, 200))
        dp.reactive_train_data.watch(lambda: gui_helper.updateLabels(dp.reactive_train_data.value[0][2], train_label))

        stops_label = Label(main_frame, text="", fg='white', bg='#061f36', anchor='w', justify=LEFT, font=('Calibri Light', 15))
        stops_label.grid(row=1, column=2, rowspan=5, sticky="NSEW")
        dp.reactive_train_data.watch(lambda: updateStopsOnStations())

        passing_label = Label(self.root, text="Passing train incoming. Stay away from the platform",
                              fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        announcement_label = Label(self.root, text="", fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        announcement_label.grid(row=2, column=0, sticky="NSEW", pady=(0, 7))
        dp.reactive_announcements.watch(lambda: updateNotification())
        dp.reactive_passing.watch(lambda: updateNotification())

        warning_label = Label(warning_frame, text="", fg='red', bg='#0a4a70', font=('Calibri Light', 15))
        warning_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        dp.reactive_warnings.watch(lambda: updateNotification())

        # Method for going through Notifications
        def handleNotifications():
            # Loops through the announcements
            self.announcement_id = gui_helper.changeNotification(self.announcement_id, announcement_label, dp.reactive_announcements.value)
            # Loops through the warnings
            self.warning_id = gui_helper.changeNotification(self.warning_id, warning_label, dp.reactive_warnings.value)
            self.root.after(10000, handleNotifications)

        def updateNotification():
            # shows passing alert if there is a passing train
            if dp.reactive_passing.value:
                announcement_label.grid_forget()
                passing_label.grid(row=2, column=0, sticky="NSEW", pady=(0, 7))
            # if else show announcement label
            elif len(dp.reactive_announcements.value) > 0:
                passing_label.grid_forget()
                announcement_label.grid(row=2, column=0, sticky="NSEW", pady=(0, 7))
            # shows warning alert of there are any
            gui_helper.showWarning(main_frame, warning_frame, dp.reactive_warnings.value)

        def updateStopsOnStations():
            text = ""
            for station in dp.reactive_train_data.value[0][5]:
                text += "  ◦ " + station + "\n"
            stops_label.config(text=text)

        def updateScreen():
            dp.checkPassingTrain()
            time_label['text'] = datetime.now().strftime("%H:%M:%S")
            gui_helper.checkResize(self.root, resizeFonts)
            self.root.after(1000, updateScreen)

        def resizeFonts(sizes):
            display_name_label['font'] = ('Calibri Light', sizes['md'])
            announcement_label['font'] = ('Calibri Light', sizes['md'])
            passing_label['font'] = ('Calibri Light', sizes['md'])
            warning_label['font'] = ('Calibri Light', sizes['lg'])
            time_label['font'] = ('Calibri Light', sizes['md'])
            arrive_label['font'] = ('Calibri Light', sizes['lg'])
            destination_label['font'] = ('Calibri Light', sizes['xxl'])
            train_label['font'] = ('Calibri Light', sizes['xxl'])
            stops_label['font'] = ('Calibri Light', sizes['md'])

        top_frame.grid(row=0, column=0, sticky="NSEW")
        warning_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.tkraise()

        handleNotifications()
        updateScreen()
        self.root.mainloop()
