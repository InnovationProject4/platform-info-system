import tkinter as tk
from tkinter import ttk


def createAnnouncementManager(left_frame):
    announcement_frame = tk.Frame(left_frame, bg='#b8b8b8')
    announcement_frame.grid(row=0, column=0, sticky='NSEW')

    tk.Grid.columnconfigure(announcement_frame, 0, weight=1)
    tk.Grid.columnconfigure(announcement_frame, 1, weight=1)
    tk.Grid.columnconfigure(announcement_frame, 2, weight=1)
    tk.Grid.columnconfigure(announcement_frame, 3, weight=1)
    tk.Grid.columnconfigure(announcement_frame, 4, weight=1)
    tk.Grid.columnconfigure(announcement_frame, 5, weight=1)
    tk.Grid.rowconfigure(announcement_frame, 0, weight=1)
    tk.Grid.rowconfigure(announcement_frame, 1, weight=1)
    tk.Grid.rowconfigure(announcement_frame, 2, weight=6)
    tk.Grid.rowconfigure(announcement_frame, 3, weight=1)

    tk.Label(announcement_frame, text="Notify type", bg="#b8b8b8").grid(row=0, column=0, sticky='NSEW', padx=(10, 10))
    type_box = ttk.Combobox(announcement_frame, values=["cancelled", "delayed", "alert", "global"], width=6)
    type_box.grid(row=0, column=1, sticky='EW')

    tk.Label(announcement_frame, text="Station code", bg="#b8b8b8").grid(row=0, column=2, sticky='NSEW', padx=(10, 10))
    station_entry = tk.Entry(announcement_frame, width=5)
    station_entry.grid(row=0, column=3, sticky='EW')

    tk.Label(announcement_frame, text="Platfrom id", bg="#b8b8b8").grid(row=0, column=4, sticky='NSEW', padx=(10, 10))
    platform_entry = tk.Entry(announcement_frame, width=5)
    platform_entry.grid(row=0, column=5, sticky='EW', padx=(0, 10))

    announcement_entry = tk.Entry(announcement_frame)
    announcement_entry.grid(row=1, column=0, sticky='EW', columnspan=5, padx=(10, 10))

    add_button = tk.Button(announcement_frame, text="Add")
    add_button.grid(row=1, column=5, sticky='EW', padx=(0, 10))

    announcement_canvas = tk.Canvas(announcement_frame, bg="light blue", height=5)
    announcement_canvas.grid(row=2, column=0, columnspan=6, sticky='NSEW')

    update_button = tk.Button(announcement_frame, text="Update")
    update_button.grid(row=3, column=0, columnspan=6, sticky='NSEW')

    tk.Label(left_frame, text="Information display manager", font=('Calibri Light', 15)).grid(row=1, column=0,
                                                                                              sticky='NSEW')