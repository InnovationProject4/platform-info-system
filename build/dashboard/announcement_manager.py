import tkinter as tk
from tkinter import ttk
import dashboard.controller as controller

announcement_canvas_data = []


def createAnnouncementManager(left_frame, root):

    # creates announcement_frame to left_frame
    announcement_frame = tk.Frame(left_frame, bg='#d8d8d8')
    announcement_frame.grid(row=0, column=0, sticky='NSEW')

    # configures the grid layout (Canvas has a weight of 6)
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

    # creating entry fields for inputting notify type, station code and platform
    tk.Label(announcement_frame, text="Notify type*", bg="#d8d8d8").grid(row=0, column=0, sticky='NSEW', padx=(10, 10))
    type_box = ttk.Combobox(announcement_frame, state="readonly", values=["info", "alert"], width=6)
    type_box.grid(row=0, column=1, sticky='EW')

    tk.Label(announcement_frame, text="Station code*", bg="#d8d8d8").grid(row=0, column=2, sticky='NSEW', padx=(10, 10))
    station_entry = tk.Entry(announcement_frame, width=5)
    station_entry.grid(row=0, column=3, sticky='EW')

    tk.Label(announcement_frame, text="Platfrom id", bg="#d8d8d8").grid(row=0, column=4, sticky='NSEW', padx=(10, 10))
    platform_entry = tk.Entry(announcement_frame, width=5)
    platform_entry.grid(row=0, column=5, sticky='EW', padx=(0, 10))

    # creating the entry for adding a new announcement
    announcement_entry = tk.Entry(announcement_frame)
    announcement_entry.grid(row=1, column=0, sticky='EW', columnspan=5, padx=(10, 10))

    # Including a scrollbar if the announcements go off the canvas
    scrollbar = tk.Scrollbar(announcement_frame)
    announcement_canvas = tk.Canvas(announcement_frame, height=200, yscrollcommand=scrollbar.set)
    table_frame = tk.Frame(announcement_canvas)

    # Add button which adds a row to the canvas and adds the row_frame elements to announcement_canvas_data
    add_button = tk.Button(announcement_frame, text="Add",
                           command=lambda: controller.addRow(table_frame, announcement_canvas_data,
                                                              announcement_entry))
    add_button.grid(row=1, column=5, sticky='EW', padx=(0, 10))

    scrollbar.grid(row=0, column=6, sticky="NS", rowspan=4)
    announcement_canvas.grid(row=2, column=0, columnspan=6, sticky='NSEW')
    scrollbar.config(command=announcement_canvas.yview)

    # creates a "window" frame on top of the canvas so the scrollbar can be implemented
    announcement_canvas.create_window((0, 0), window=table_frame, anchor='nw', tags="frame")
    table_frame.bind('<Configure>', lambda e: announcement_canvas.configure(scrollregion=announcement_canvas.bbox('all')))

    # adds a bind to the canvas so the canvas height and width are responsive
    def canvasBind(e):
        announcement_canvas.configure(height=round(root.winfo_height() / 6))
        announcement_canvas.itemconfig('frame', width=announcement_canvas.winfo_width())

    announcement_canvas.bind('<Configure>', canvasBind)

    # updates the announcements to db
    def handleUpdate():
        global announcement_canvas_data
        topic = f"announcement/{type_box.get()}/{station_entry.get()}"
        if platform_entry.get() != '':
            topic += f"/{platform_entry.get()}"
        controller.dbSet(announcement_canvas_data, topic)

    update_button = tk.Button(announcement_frame, text="Update", state=tk.DISABLED, command=lambda: handleUpdate())
    update_button.grid(row=3, column=0, columnspan=6, sticky='NSEW', pady=7, padx=7)

    # validates the entries and gets announcements from the db
    def handleFindButton():
        pass
        global announcement_canvas_data
        if not controller.validateEntries([station_entry, type_box]):
            return
        update_button.config(state=tk.NORMAL)
        display_find.master.focus()
        display_find.grid_forget()
        if platform_entry.get() == "":
            items = controller.dbGet(f"announcement/{type_box.get()}/{station_entry.get()}")
        else:
            items = controller.dbGet(f"announcement/{type_box.get()}/{station_entry.get()}/{platform_entry.get()}")
        controller.fillRows(table_frame, announcement_canvas_data, items)

    # By default the button is shown on top of message entry and add button
    display_find = tk.Button(announcement_frame, text="Find display", command=handleFindButton)
    display_find.grid(row=1, column=0, sticky='EW', columnspan=6, padx=(10, 10))

    # Adds binds to all entries which clear the canvas and reset display find button
    def entryBind():
        global announcement_canvas_data
        announcement_canvas_data = []
        controller.deleteAllRows(table_frame)
        update_button.config(state=tk.DISABLED)
        display_find.grid(row=1, column=0, sticky='EW', columnspan=6, padx=(10, 10))

    station_entry.bind('<FocusIn>', lambda e: entryBind())
    platform_entry.bind('<FocusIn>', lambda e: entryBind())
    type_box.bind('<FocusIn>', lambda e: entryBind())

    tk.Label(left_frame, text="Information display manager", font=('Calibri Light', 15)).grid(row=1, column=0,
                                                                                              sticky='NSEW')
