import tkinter as tk
import dashboard.controller as controller


def createInfodisplayManager(left_frame, root):
    # Creating infodisplay_frame to left_frame
    infodisplay_frame = tk.Frame(left_frame, bg='#d8d8d8')
    infodisplay_frame.grid(row=2, column=0, sticky='NSEW')

    # Configuring the grid layout (Canvas has weight 6)
    tk.Grid.columnconfigure(infodisplay_frame, 0, weight=1)
    tk.Grid.columnconfigure(infodisplay_frame, 1, weight=1)
    tk.Grid.rowconfigure(infodisplay_frame, 0, weight=1)
    tk.Grid.rowconfigure(infodisplay_frame, 1, weight=1)
    tk.Grid.rowconfigure(infodisplay_frame, 2, weight=6)
    tk.Grid.rowconfigure(infodisplay_frame, 3, weight=1)

    tk.Label(infodisplay_frame, text="Station code*", bg="#d8d8d8").grid(row=0, column=0, sticky='NSE')

    station_entry = tk.Entry(infodisplay_frame, width=5)
    station_entry.grid(row=0, column=1, sticky='W', columnspan=2, padx=(10, 0))

    announcement_entry = tk.Entry(infodisplay_frame)
    announcement_entry.grid(row=1, column=0, sticky='EW', columnspan=2, padx=(10, 10))

    infodisplay_canvas_data = []

    scrollbar = tk.Scrollbar(infodisplay_frame)
    infodisplay_canvas = tk.Canvas(infodisplay_frame, height=200, yscrollcommand=scrollbar.set)
    table_frame = tk.Frame(infodisplay_canvas)

    add_button = tk.Button(infodisplay_frame, text="Add",
                           command=lambda: controller.add_row(table_frame, infodisplay_canvas_data,
                                                              announcement_entry))

    add_button.grid(row=1, column=2, sticky='EW', padx=(0, 10))

    scrollbar.grid(row=0, column=3, sticky="NS", rowspan=4)
    infodisplay_canvas.grid(row=2, column=0, columnspan=3, sticky='NSEW')
    scrollbar.config(command=infodisplay_canvas.yview)

    infodisplay_canvas.create_window((0, 0), window=table_frame, anchor='nw', tags="frame")
    table_frame.bind('<Configure>', lambda e: infodisplay_canvas.configure(scrollregion=infodisplay_canvas.bbox('all')))

    def canvasBind(e):
        infodisplay_canvas.configure(height=round(root.winfo_height() / 6))
        infodisplay_canvas.itemconfig('frame', width=infodisplay_canvas.winfo_width())

    infodisplay_canvas.bind('<Configure>', canvasBind)

    update_button = tk.Button(infodisplay_frame, text="Update")
    update_button.grid(row=3, column=0, columnspan=3, sticky='NSEW')
