import tkinter as tk

from messaging.telemetry import Connection

conn = Connection("localhost", 1883)
conn.connect()


def add_row(frame, data, entry):
    if entry.get() == "":  # returns if entry is empty
        return

    # creates a new row of widgets
    row_frame = tk.Frame(frame, bg="#cccccc")
    tk.Grid.columnconfigure(row_frame, 0, weight=1)
    message = tk.Label(row_frame, text=entry.get(), font=('Calibri Light', 9))

    # binds message so it doesn't go past the frame nor the delete button
    message.bind('<Configure>', lambda e: message.configure(wraplength=(row_frame.winfo_width() - 80)))
    delete_button = tk.Button(row_frame, text='Delete', command=lambda: delete_row(row_frame, data))

    # packs the widgets into the row frame
    message.grid(row=0, column=0, padx=10, pady=4)
    delete_button.grid(row=0, column=1, sticky="E", padx=(0, 10), pady=4)

    # adds the row to the table
    data.append((message, delete_button))
    row_frame.pack(fill="x", expand=True, pady=2)

    # empties the entry when you add a message
    entry.delete(0, tk.END)


def delete_row(row_frame, data):
    # removes the row from the table
    for row_data in data:
        if row_data[0].master == row_frame:
            data.remove(row_data)
            break

    # destroys the row's widgets
    row_frame.destroy()


def insertToLog(log, msg):
    log.configure(state="normal")
    log.insert(tk.END, msg)
    log.see(tk.END)
    log.configure(state="disabled")


def connectToDisplays(log):
    conn.subscribe_multiple([
        ("management/#", lambda client, userdata, message: (
            insertToLog(log, f"{message.payload.decode()}\n")
        ))])


def connectToAggregator(log):
    conn.subscribe_multiple([
        ("station/#", lambda client, userdata, message: (
            insertToLog(log, f"Publish: {message.topic}\n")
        ))])
