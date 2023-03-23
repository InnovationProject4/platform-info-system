from tkinter import *
import threading
from display import gui_helper, display_printer as dp, mqtt_connection as mqtt
from datetime import datetime


class App(threading.Thread):

    def __init__(self, warning_id=0):
        self.warning_id = warning_id
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
        Grid.rowconfigure(self.root, 1, weight=20)

        top_frame = Frame(self.root, bg='#0a4a70')
        main_frame = Frame(self.root, bg='black')
        warning_frame = Frame(self.root, bg='#0a4a70')

        Grid.columnconfigure(top_frame, 0, weight=1)
        Grid.columnconfigure(top_frame, 1, weight=1)
        Grid.rowconfigure(top_frame, 0, weight=1)
        Grid.columnconfigure(main_frame, 0, weight=1)
        Grid.rowconfigure(main_frame, 0, weight=1)

        display_name_label = Label(top_frame, text="🛈 Info", fg='white', bg='#0a4a70', font=('Calibri Light', 25))
        display_name_label.grid(row=0, column=0, sticky="W", padx=(20, 0))

        time_label = Label(top_frame, text="", fg='white', bg='#0a4a70', font=('Calibri Light', 15))
        time_label.grid(row=0, column=1, sticky="E", padx=(0, 20))

        warning_label = Label(warning_frame, text="", fg='red', bg='#0a4a70', font=('Calibri Light', 15))
        warning_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        dp.reactive_warnings.watch(lambda: updateNotification())

        announcements_label = Label(main_frame, text="", fg='white', bg='#031926', justify="left", font=('Calibri Light', 15))
        announcements_label.grid(row=0, column=0, sticky="wens", padx=10, pady=10, )
        announcements_label.bind('<Configure>',
                         lambda e: announcements_label.configure(wraplength=self.root.winfo_width()))
        dp.reactive_announcements.watch(lambda: updateNotification())

        # Method for going through the different Notifications
        def changeNotification():
            # Loops through the warnings
            if self.warning_id >= len(dp.reactive_warnings.value):
                self.warning_id = 0
            if len(dp.reactive_warnings.value) > 0:
                warning_label.config(text=dp.reactive_warnings.value[self.warning_id])
            self.warning_id += 1

            self.root.after(10000, changeNotification)

        def updateNotification():
            # shows warning alert of there are any
            if len(dp.reactive_warnings.value) > 0 and dp.reactive_warnings.value[0] != '':
                warning_frame.tkraise()
            else:
                main_frame.tkraise()

            # displays announcements
            if len(dp.reactive_announcements.value) > 0 and dp.reactive_announcements.value[0] != '':
                text = ""
                for announcement in dp.reactive_announcements.value:
                    text += '◦ ' + announcement + '\n\n'
                announcements_label.configure(text=text)

        def updateScreen():
            time_label['text'] = datetime.now().strftime("%H:%M:%S")
            checkResize()
            self.root.after(1000, updateScreen)

        def checkResize():
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            if w > 1500 and h > 500:
                resizeFonts(50, 40, 40, 45)
                return
            elif w > 1000 and h > 500:
                resizeFonts(45, 35, 35, 30)
                return
            elif w > 600 and h > 400:
                resizeFonts(35, 25, 25, 20)
                return
            elif w > 300 and h > 200:
                resizeFonts(25, 15, 15, 15)
                return

        def resizeFonts(s_name, s_warning, s_time, s_info):
            display_name_label['font'] = ('Calibri Light', s_name)
            warning_label['font'] = ('Calibri Light', s_warning)
            time_label['font'] = ('Calibri Light', s_time)
            announcements_label['font'] = ('Calibri Light', s_info)

        top_frame.grid(row=0, column=0, sticky="NSEW")
        warning_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.grid(row=1, column=0, sticky="NSEW")
        main_frame.tkraise()

        changeNotification()
        updateScreen()
        self.root.mainloop()
