import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("1280x720")

# Configures the amount of columns and rows for root
tk.Grid.columnconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 1, weight=1)
tk.Grid.columnconfigure(root, 2, weight=1)
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.rowconfigure(root, 1, weight=60)

# Adding labels to top of the root
tk.Label(root, text="Announcement manager", font=('Calibri Light', 15)).grid(row=0, column=0, sticky='NSEW')
tk.Label(root, text="Management log", font=('Calibri Light', 15)).grid(row=0, column=1, sticky='NSEW')
tk.Label(root, text="Status log", font=('Calibri Light', 15)).grid(row=0, column=2, sticky='NSEW')

# Creates and adds 3 frames inside the root frame
left_frame = tk.Frame(root, bg='#b8b8b8')
left_frame.grid(row=1, column=0, sticky='NSEW')
middle_frame = tk.Frame(root, bg='#141414')
middle_frame.grid(row=1, column=1, sticky='NSEW')
right_frame = tk.Frame(root, bg='#141414')
right_frame.grid(row=1, column=2, sticky='NSEW')

# Configures the amount of columns and rows for frames
tk.Grid.columnconfigure(right_frame, 0, weight=1)
tk.Grid.rowconfigure(right_frame, 0, weight=1)
tk.Grid.columnconfigure(middle_frame, 0, weight=1)
tk.Grid.rowconfigure(middle_frame, 0, weight=1)
tk.Grid.columnconfigure(left_frame, 0, weight=1)
tk.Grid.rowconfigure(left_frame, 0, weight=70)
tk.Grid.rowconfigure(left_frame, 1, weight=1)
tk.Grid.rowconfigure(left_frame, 2, weight=70)

# Creates a display status log with a scrollbar inside the right frame
status_log = tk.Text(right_frame, bg='#141414', fg='white', highlightthickness=0, borderwidth=0,
                     font=('Calibri Light', 13))
status_log.configure(state="disabled")
status_log.grid(row=0, column=0, sticky='NSEW', padx=(20, 20), pady=(20, 20))
scrollbar = tk.Scrollbar(right_frame, command=status_log.yview)
scrollbar.grid(row=0, column=1, sticky='NSEW')
status_log.config(yscrollcommand=scrollbar.set)

# Creates a management log with a scrollbar inside the middle frame
management_log = tk.Text(middle_frame, bg='#141414', fg='white', highlightthickness=0, borderwidth=0,
                         font=('Calibri Light', 13))
management_log.configure(state="disabled")
management_log.grid(row=0, column=0, sticky='NSEW', padx=(20, 20), pady=(20, 20))
scrollbar = tk.Scrollbar(middle_frame, command=management_log.yview)
scrollbar.grid(row=0, column=1, sticky='NSEW')
management_log.config(yscrollcommand=scrollbar.set)

# ------------------- ANNOUNCEMENT FRAME -------------------

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

# ------------------- INFODISPLAY FRAME -------------------

infodisplay_frame = tk.Frame(left_frame, bg='#b8b8b8')
infodisplay_frame.grid(row=2, column=0, sticky='NSEW')

tk.Grid.columnconfigure(infodisplay_frame, 0, weight=1)
tk.Grid.columnconfigure(infodisplay_frame, 1, weight=1)
tk.Grid.rowconfigure(infodisplay_frame, 0, weight=1)
tk.Grid.rowconfigure(infodisplay_frame, 1, weight=1)
tk.Grid.rowconfigure(infodisplay_frame, 2, weight=6)
tk.Grid.rowconfigure(infodisplay_frame, 3, weight=1)

station_label = tk.Label(infodisplay_frame, text="Station code", bg="#b8b8b8").grid(row=0, column=0, sticky='NSE')

station_entry = tk.Entry(infodisplay_frame, width=5)
station_entry.grid(row=0, column=1, sticky='W', columnspan=2, padx=(10, 0))

announcement_entry = tk.Entry(infodisplay_frame)
announcement_entry.grid(row=1, column=0, sticky='EW', columnspan=2, padx=(10, 10))

infodisplay_canvas_data = []

def addToInfo():
    # creates a new row of widgets
    row_frame = tk.Frame(table_frame)
    message = tk.Label(row_frame, text="Testasdasdasdasdasdasdaasdasdsadasdasdasadi")
    delete_button = tk.Button(row_frame, text='Delete', command=lambda: delete_row(row_frame))

    # packs the widgets into the row frame
    message.pack(side=tk.LEFT, padx=5)
    delete_button.pack(side=tk.RIGHT, padx=5)

    # adds the row to the table
    infodisplay_canvas_data.append((message, delete_button))
    row_frame.pack()


def delete_row(row_frame):
    # removes the row from the table
    for row_data in infodisplay_canvas_data:
        if row_data[0].master == row_frame:
            infodisplay_canvas_data.remove(row_data)
            break

    # destroys the row's widgets
    row_frame.destroy()


def FrameWidth(self, event):
        canvas_width = event.width
        self.infodisplay_canvas.itemconfig(self.table_frame, width=canvas_width)


add_button = tk.Button(infodisplay_frame, text="Add", command=addToInfo)
add_button.grid(row=1, column=2, sticky='EW', padx=(0, 10))

info_scrollbar = tk.Scrollbar(infodisplay_frame)
info_scrollbar.grid(row=0, column=3, sticky="NS", rowspan=4)
infodisplay_canvas = tk.Canvas(infodisplay_frame, bg="light blue", height=200, yscrollcommand=info_scrollbar.set)
infodisplay_canvas.grid(row=2, column=0, columnspan=3, sticky='NSEW')
info_scrollbar.config(command=infodisplay_canvas.yview)

table_frame = tk.Frame(infodisplay_canvas)
infodisplay_canvas.create_window((0, 0), window=table_frame, anchor='nw') ##
table_frame.bind('<Configure>', lambda e: infodisplay_canvas.configure(scrollregion=infodisplay_canvas.bbox('all')))

update_button = tk.Button(infodisplay_frame, text="Update")
update_button.grid(row=3, column=0, columnspan=3, sticky='NSEW')

i = 0


def insertMsg():
    global i
    i += 1
    status_log.configure(state="normal")
    status_log.insert(tk.END, f"Display connected test {i}\n")
    status_log.see(tk.END)
    status_log.configure(state="disabled")


butt = tk.Button(root, text="Test", command=lambda: [insertMsg(), addToInfo()])
butt.grid(row=0, column=3, sticky='NSEW')


def updateScreen():
    root.after(1000, updateScreen)
    management_log['width'] = round(root.winfo_width() / 40)
    status_log['width'] = round(root.winfo_width() / 40)
    infodisplay_canvas['height'] = round(root.winfo_height() / 6)
    announcement_canvas['height'] = round(root.winfo_height() / 6)


updateScreen()
root.mainloop()
