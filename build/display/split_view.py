from tkinter import *
import threading
from display import gui_helper, display_printer as dp
from datetime import datetime


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
        # self.root.attributes('-fullscreen', True)
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 1, weight=7)

        top_frame = Frame(self.root, bg='#0a4a70')
        main_frame = Frame(self.root, bg='#2788c2')
        warning_frame = Frame(self.root, bg='#0a4a70')

        Grid.columnconfigure(top_frame, 0, weight=1)
        Grid.columnconfigure(top_frame, 1, weight=1)
        Grid.rowconfigure(top_frame, 0, weight=1)
        Grid.columnconfigure(main_frame, 0, weight=25)
        Grid.columnconfigure(main_frame, 1, weight=1)
        Grid.columnconfigure(main_frame, 2, weight=25)
        Grid.rowconfigure(main_frame, 0, weight=1)

        display_name_label = Label(top_frame, text=dp.reactive_display_name.value, fg='white', bg='#0a4a70', font=('Calibri Light', 25))
        display_name_label.grid(row=0, column=0, sticky="W", padx=(20, 0))
        dp.reactive_display_name.watch(lambda: updateLabels(dp.reactive_display_name, display_name_label))

        time_label = Label(top_frame, text="", fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        time_label.grid(row=0, column=1, sticky="E", padx=(0, 20))

        notification_label = Label(self.root, text=dp.reactive_notification.value, fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        notification_label.grid(row=2, column=0, sticky="NSEW", pady=(0, 7))
        dp.reactive_notification.watch(lambda: updateLabels(dp.reactive_notification, notification_label))

        warning_label = Label(warning_frame, text="", fg='red', bg='#0a4a70', font=('Calibri Light', 15))
        warning_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        dp.reactive_warning.watch(lambda: updateLabels(dp.reactive_warning, warning_label))

        leftframe = Frame(main_frame, bg='#36a8eb')
        leftframe.grid(row=0, column=0, sticky="NSEW")
        rightframe = Frame(main_frame, bg='#36a8eb')
        rightframe.grid(row=0, column=2, sticky="NSEW")

        left_labels = gui_helper.configureDualPlatformGrid(leftframe, Grid, gui_helper.fillLeftSide)
        dp.reactive_train_data.watch(lambda: updateTrains(dp.reactive_train_data, left_labels))
        right_labels = gui_helper.configureDualPlatformGrid(rightframe, Grid, gui_helper.fillRightSide)
        dp.reactive_train_data2.watch(lambda: updateTrains(dp.reactive_train_data2, right_labels))

        def updateLabels(reactive, label):
            label.config(text=reactive.value)

        def updateTrains(reactive, labels):
            i = 0
            for label in labels:
                try:
                    if (i+1) == 1 and reactive.value[0][1] != "":
                        label['text'] = reactive.value[0][0] + reactive.value[0][1]
                        i += 1
                    elif i == 0:
                        label['text'] = reactive.value[0][i]
                        i += 1
                    else:
                        label['text'] = reactive.value[0][i]
                    i += 1
                except IndexError:
                    label['text'] = ''

        def updateScreen():
            if dp.reactive_warning.value != '':
                warning_frame.tkraise()
            else:
                main_frame.tkraise()
            time_label['text'] = datetime.now().strftime("%H:%M:%S")
            checkResize()
            self.root.after(1000, updateScreen)

        def checkResize():
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            if w > 1500 and h > 500:
                resizeFonts(40, 40, 40, 55, 35)
                return
            elif w > 1000 and h > 500:
                resizeFonts(35, 35, 35, 45, 25)
                return
            elif w > 600 and h > 400:
                resizeFonts(25, 25, 25, 35, 15)
                return
            elif w > 300 and h > 200:
                resizeFonts(15, 15, 15, 30, 10)
                return

        def resizeFonts(s_name, s_warning, s_time, s_trains, s_notification):
            display_name_label['font'] = ('Calibri Light', s_name)
            notification_label['font'] = ('Calibri Light', s_notification)
            warning_label['font'] = ('Calibri Light', s_warning)
            time_label['font'] = ('Calibri Light', s_time)
            for lLabel, rLabel in zip(left_labels, right_labels):
                lLabel['font'] = ('Calibri Light', s_trains)
                rLabel['font'] = ('Calibri Light', s_trains)

        top_frame.grid(row=0, column=0, sticky="NSEW")
        warning_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.tkraise()

        updateScreen()
        self.root.mainloop()
