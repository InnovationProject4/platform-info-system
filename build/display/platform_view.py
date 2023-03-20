from tkinter import *
import threading
from display import gui_helper, display_printer as dp, mqtt_connection as mqtt
from datetime import datetime


class App(threading.Thread):

    def __init__(self, announcement_id=0):
        self.announcement_id = announcement_id
        threading.Thread.__init__(self)
        self.root = None
        self.start()

    def callback(self):
        self.root.quit()

    def onClose(self):
        mqtt.onDisconnect()
        self.callback()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.root['bg'] = '#0a4a70'
        self.root.geometry("640x360")
        # self.root.attributes('-fullscreen', True)
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
        dp.reactive_display_name.watch(lambda: updateLabels(dp.reactive_display_name.value, display_name_label))

        time_label = Label(top_frame, text="", fg='white', bg='#031626', font=('Calibri Light', 15))
        time_label.grid(row=0, column=1, sticky="E", padx=(0, 20))

        Grid.columnconfigure(main_frame, 0, weight=2)
        Grid.columnconfigure(main_frame, 1, weight=1)
        Grid.columnconfigure(main_frame, 2, weight=2)

        arrive_label = Label(main_frame, text="", fg='white', anchor='e', justify=RIGHT, bg='#061f36', font=('Calibri Light', 15))
        arrive_label.grid(row=0, column=0, sticky="SEW")
        dp.reactive_train_data.watch(lambda: updateLabels(dp.reactive_train_data.value[0][0], arrive_label))

        destination_label = Label(main_frame, text="", anchor='e', justify=RIGHT, fg='white', bg='#061f36', font=('Calibri Light', 30))
        destination_label.grid(row=1, column=0, sticky="NSEW")
        dp.reactive_train_data.watch(lambda: updateLabels(dp.reactive_train_data.value[0][3], destination_label))

        train_label = Label(main_frame, text="", anchor='e', justify=RIGHT, fg='white', bg='#061f36', font=('Calibri Light', 35))
        train_label.grid(row=0, column=2, sticky="NSEW", padx=(0, 100))
        dp.reactive_train_data.watch(lambda: updateLabels(dp.reactive_train_data.value[0][2], train_label))

        # TODO stop label
        stops_label = Label(main_frame, text="Test\nTest\nTest\nTest", fg='white', bg='#061f36', anchor='w', justify=LEFT, font=('Calibri Light', 15))
        stops_label.grid(row=1, column=2, rowspan=9, sticky="NSEW")

        passing_label = Label(self.root, text="Passing train incoming. Stay away from the platform",
                              fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        announcement_label = Label(self.root, text="", fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        announcement_label.grid(row=2, column=0, sticky="NSEW", pady=(0, 7))
        dp.reactive_announcements.watch(lambda: updateNotification())
        dp.reactive_passing.watch(lambda: updateNotification())

        warning_label = Label(warning_frame, text="", fg='red', bg='#0a4a70', font=('Calibri Light', 15))
        warning_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        dp.reactive_warning.watch(lambda: updateLabels(dp.reactive_warning.value, warning_label))

        # method for going through the different announcements
        def changeAnnouncement():
            if self.announcement_id >= len(dp.reactive_announcements.value):
                self.announcement_id = 0
            if len(dp.reactive_announcements.value) > 0:
                announcement_label.config(text=dp.reactive_announcements.value[self.announcement_id])
            self.announcement_id += 1
            self.root.after(10000, changeAnnouncement)

        def updateNotification():
            # shows passing alert if there is a passing train
            if dp.reactive_passing.value:
                announcement_label.grid_forget()
                passing_label.grid(row=2, column=0, sticky="NSEW", pady=(0, 7))
            elif len(dp.reactive_announcements.value) > 0:
                passing_label.grid_forget()
                announcement_label.grid(row=2, column=0, sticky="NSEW", pady=(0, 7))

        def updateLabels(reactive, label):
            label.config(text=reactive)

        def updateScreen():
            if dp.reactive_warning.value != '':
                warning_frame.tkraise()
            else:
                main_frame.tkraise()
            dp.checkPassingTrain()
            time_label['text'] = datetime.now().strftime("%H:%M:%S")
            checkResize()
            self.root.after(1000, updateScreen)

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
            announcement_label['font'] = ('Calibri Light', s_notification)
            passing_label['font'] = ('Calibri Light', s_notification)
            warning_label['font'] = ('Calibri Light', s_warning)
            time_label['font'] = ('Calibri Light', s_time)
            arrive_label['font'] = ('Calibri Light', s_arrive)
            destination_label['font'] = ('Calibri Light', s_platform)
            train_label['font'] = ('Calibri Light', s_platform)
            stops_label['font'] = ('Calibri Light', s_stops)

        top_frame.grid(row=0, column=0, sticky="NSEW")
        warning_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.tkraise()

        changeAnnouncement()
        updateScreen()
        self.root.mainloop()
