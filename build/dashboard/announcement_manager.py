import tkinter as tk
from tkinter import ttk
import dashboard.controller as controller

def createAnnouncementManager(left_frame, root):
    announcement_frame = tk.Frame(left_frame, bg='#d8d8d8')
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

    tk.Label(announcement_frame, text="Notify type*", bg="#d8d8d8").grid(row=0, column=0, sticky='NSEW', padx=(10, 10))
    type_box = ttk.Combobox(announcement_frame, values=["cancelled", "delayed", "alert", "global"], width=6)
    type_box.grid(row=0, column=1, sticky='EW')

    tk.Label(announcement_frame, text="Station code*", bg="#d8d8d8").grid(row=0, column=2, sticky='NSEW', padx=(10, 10))
    station_entry = tk.Entry(announcement_frame, width=5)
    station_entry.grid(row=0, column=3, sticky='EW')

    tk.Label(announcement_frame, text="Platfrom id", bg="#d8d8d8").grid(row=0, column=4, sticky='NSEW', padx=(10, 10))
    platform_entry = tk.Entry(announcement_frame, width=5)
    platform_entry.grid(row=0, column=5, sticky='EW', padx=(0, 10))

    announcement_entry = tk.Entry(announcement_frame)
    announcement_entry.grid(row=1, column=0, sticky='EW', columnspan=5, padx=(10, 10))

    announcement_canvas_data = []

    scrollbar = tk.Scrollbar(announcement_frame)
    announcement_canvas = tk.Canvas(announcement_frame, height=200, yscrollcommand=scrollbar.set)
    table_frame = tk.Frame(announcement_canvas)

    add_button = tk.Button(announcement_frame, text="Add",
                           command=lambda: controller.add_row(table_frame, announcement_canvas_data,
                                                              announcement_entry))

    add_button.grid(row=1, column=5, sticky='EW', padx=(0, 10))

    scrollbar.grid(row=0, column=6, sticky="NS", rowspan=4)
    announcement_canvas.grid(row=2, column=0, columnspan=6, sticky='NSEW')
    scrollbar.config(command=announcement_canvas.yview)

    announcement_canvas.create_window((0, 0), window=table_frame, anchor='nw', tags="frame")
    table_frame.bind('<Configure>', lambda e: announcement_canvas.configure(scrollregion=announcement_canvas.bbox('all')))

    def canvasBind(e):
        announcement_canvas.configure(height=round(root.winfo_height() / 6))
        announcement_canvas.itemconfig('frame', width=announcement_canvas.winfo_width())

    announcement_canvas.bind('<Configure>', canvasBind)

    update_button = tk.Button(announcement_frame, text="Update")
    update_button.grid(row=3, column=0, columnspan=6, sticky='NSEW')

    tk.Label(left_frame, text="Information display manager", font=('Calibri Light', 15)).grid(row=1, column=0,
                                                                                              sticky='NSEW')
