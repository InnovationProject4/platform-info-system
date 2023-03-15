import tkinter as tk


def add_row(frame, data):
    # creates a new row of widgets
    row_frame = tk.Frame(frame, bg="#cccccc")
    message = tk.Label(row_frame, text="Tönöön on paljon perumisia jasdasdas asdasdasd", font=('Calibri Light', 9))
    delete_button = tk.Button(row_frame, text='Delete', command=lambda: delete_row(row_frame, data))

    # packs the widgets into the row frame
    message.pack(padx=5, fill="x", side=tk.LEFT)
    delete_button.pack(padx=5, fill="x", side=tk.RIGHT)

    # adds the row to the table
    data.append((message, delete_button))
    row_frame.pack(fill="x", expand=True)


def delete_row(row_frame, data):
    # removes the row from the table
    for row_data in data:
        if row_data[0].master == row_frame:
            data.remove(row_data)
            break

    # destroys the row's widgets
    row_frame.destroy()
