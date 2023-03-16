from tkinter import *
import threading
from display import gui_helper, display_printer as dp, mqtt_connection as mqtt
from datetime import datetime


class App(threading.Thread):

    def __init__(self, column_labels, rowcount):
        self.column_labels = column_labels
        self.rowcount = rowcount
        threading.Thread.__init__(self)
        self.root = None
        self.start()

    def callback(self):
        self.root.quit()

    def onClose(self):
        mqtt.disconnectOnWindowClose()
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

        top_frame = Frame(self.root, bg='#0a4a70')
        main_frame = Frame(self.root, bg='#0a4a70')
        warning_frame = Frame(self.root, bg='#0a4a70')

        Grid.columnconfigure(top_frame, 0, weight=1)
        Grid.columnconfigure(top_frame, 1, weight=1)
        Grid.rowconfigure(top_frame, 0, weight=1)

        display_name_label = Label(top_frame, text=dp.reactive_display_name.value, fg='white', bg='#0a4a70', font=('Calibri Light', 25))
        display_name_label.grid(row=0, column=0, sticky="W", padx=(20, 0))
        dp.reactive_display_name.watch(lambda: updateLabels(dp.reactive_display_name, display_name_label))

        time_label = Label(top_frame, text="", fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        time_label.grid(row=0, column=1, sticky="E", padx=(0, 20))

        notification_label = Label(self.root, text=dp.reactive_notification.value, fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        notification_label.grid(row=2, column=0, sticky="NSEW", pady=(0, 7))
        dp.reactive_notification.watch(lambda: updateNotification(notification_label))
        dp.reactive_passing.watch(lambda: updateNotification(notification_label))

        warning_label = Label(warning_frame, text="", fg='red', bg='#0a4a70', font=('Calibri Light', 15))
        warning_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        dp.reactive_warning.watch(lambda: updateLabels(dp.reactive_warning, warning_label))

        gui_helper.configureGrid(main_frame, Grid, self.rowcount, self.column_labels)
        labels = gui_helper.fillGrid(main_frame, self.rowcount, self.column_labels)
        dp.reactive_train_data.watch(lambda: updateTrains(dp.reactive_train_data, labels))

        def updateNotification(label):
            if dp.reactive_passing.value:
                label.config(text="Passing train incoming. Stay away from the platform")
            else:
                label.config(text=dp.reactive_notification.value)

        def updateLabels(reactive, label):
            label.config(text=reactive.value)

        def updateTrains(reactive, tlabels):
            info, train = 0, 0
            for label in tlabels:
                try:
                    label['text'] = reactive.value[train][info]
                    info += 1
                    if info == len(reactive.value[train]):
                        info = 0
                        train += 1
                except IndexError:
                    label['text'] = ''

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
                resizeFonts(40, 40, 40, 35, 35)
                return
            elif w > 1000 and h > 500:
                resizeFonts(35, 35, 35, 25, 25)
                return
            elif w > 600 and h > 400:
                resizeFonts(25, 25, 25, 15, 15)
                return
            elif w > 300 and h > 200:
                resizeFonts(15, 15, 15, 10, 10)
                return

        def resizeFonts(s_name, s_warning, s_time, s_trains, s_notification):
            display_name_label['font'] = ('Calibri Light', s_name)
            notification_label['font'] = ('Calibri Light', s_notification)
            warning_label['font'] = ('Calibri Light', s_warning)
            time_label['font'] = ('Calibri Light', s_time)
            for label in labels:
                label['font'] = ('Calibri Light', s_trains)

        top_frame.grid(row=0, column=0, sticky="NSEW")
        warning_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.tkraise()

        updateScreen()
        self.root.mainloop()
