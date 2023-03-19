import tkinter as tk
import dashboard.controller as controller

infodisplay_canvas_data = []


def createInfodisplayManager(left_frame, root):

    # creates infodisplay_frame to left_frame
    infodisplay_frame = tk.Frame(left_frame, bg='#d8d8d8')
    infodisplay_frame.grid(row=2, column=0, sticky='NSEW')

    # configures the grid layout (Canvas has a weight of 6)
    tk.Grid.columnconfigure(infodisplay_frame, 0, weight=1)
    tk.Grid.columnconfigure(infodisplay_frame, 1, weight=1)
    tk.Grid.rowconfigure(infodisplay_frame, 0, weight=1)
    tk.Grid.rowconfigure(infodisplay_frame, 1, weight=1)
    tk.Grid.rowconfigure(infodisplay_frame, 2, weight=6)
    tk.Grid.rowconfigure(infodisplay_frame, 3, weight=1)

    # creating entry fields for inputting station code
    tk.Label(infodisplay_frame, text="Station code*", bg="#d8d8d8").grid(row=0, column=0, sticky='NSE')
    station_entry = tk.Entry(infodisplay_frame, width=5)
    station_entry.grid(row=0, column=1, sticky='W', columnspan=2, padx=(10, 0))

    # creating the entry for adding a new announcement
    announcement_entry = tk.Entry(infodisplay_frame)
    announcement_entry.grid(row=1, column=0, sticky='EW', columnspan=2, padx=(10, 10))

    # Including a scrollbar if the announcements go off the canvas
    scrollbar = tk.Scrollbar(infodisplay_frame)
    infodisplay_canvas = tk.Canvas(infodisplay_frame, height=200, yscrollcommand=scrollbar.set)
    table_frame = tk.Frame(infodisplay_canvas)

    # Add button which adds a row to the canvas and adds the row_frame elements to infodisplay_canvas_data
    add_button = tk.Button(infodisplay_frame, text="Add",
                           command=lambda: controller.addRow(table_frame, infodisplay_canvas_data,
                                                              announcement_entry))
    add_button.grid(row=1, column=2, sticky='EW', padx=(0, 10))

    scrollbar.grid(row=0, column=3, sticky="NS", rowspan=4)
    infodisplay_canvas.grid(row=2, column=0, columnspan=3, sticky='NSEW')
    scrollbar.config(command=infodisplay_canvas.yview)

    # creates a "window" frame on top of the canvas so the scrollbar can be implemented
    infodisplay_canvas.create_window((0, 0), window=table_frame, anchor='nw', tags="frame")
    table_frame.bind('<Configure>', lambda e: infodisplay_canvas.configure(scrollregion=infodisplay_canvas.bbox('all')))

    # adds a bind to the canvas so the canvas height and width are responsive
    def canvasBind(e):
        infodisplay_canvas.configure(height=round(root.winfo_height() / 6))
        infodisplay_canvas.itemconfig('frame', width=infodisplay_canvas.winfo_width())

    infodisplay_canvas.bind('<Configure>', canvasBind)

    # updates the announcements to db
    def handleUpdate():
        global infodisplay_canvas_data
        controller.dbSet(infodisplay_canvas_data, f"announcement/+/{station_entry.get()}")

    update_button = tk.Button(infodisplay_frame, text="Update", state=tk.DISABLED, command=lambda: handleUpdate())
    update_button.grid(row=3, column=0, columnspan=3, sticky='NSEW', pady=7, padx=7)

    # validates the entries and gets announcements from the db
    def handleFindButton():
        global infodisplay_canvas_data
        if not controller.validateEntries([station_entry]):
            return
        update_button.config(state=tk.NORMAL)
        display_find.master.focus()
        display_find.grid_forget()
        items = controller.dbGet(f"announcement/+/{station_entry.get()}")
        controller.fillRows(table_frame, infodisplay_canvas_data, items)

    # By default the button is shown on top of message entry and add button
    display_find = tk.Button(infodisplay_frame, text="Find display", command=handleFindButton)
    display_find.grid(row=1, column=0, sticky='EW', columnspan=3, padx=(10, 10))

    # Adds bind to station entry which clears the canvas and resets display find button
    def stationEntryBind():
        global infodisplay_canvas_data
        infodisplay_canvas_data = []
        controller.deleteAllRows(table_frame)
        update_button.config(state=tk.DISABLED)
        display_find.grid(row=1, column=0, sticky='EW', columnspan=3, padx=(10, 10))
    station_entry.bind('<FocusIn>', lambda e: stationEntryBind())



