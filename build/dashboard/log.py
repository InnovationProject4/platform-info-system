import tkinter as tk


# creates a log where messages can be inserted
def createLog(root, frame, callback):
    log = tk.Text(frame, bg='#141414', fg='white', highlightthickness=0, borderwidth=0,
                         font=('Calibri Light', 13))

    # log needs to stay disabled if messages are not inserted
    log.configure(state="disabled")
    log.grid(row=0, column=0, sticky='NSEW', padx=(20, 20), pady=(20, 20))

    # scrollbar lets the user see past messages
    scrollbar = tk.Scrollbar(frame, command=log.yview)
    scrollbar.grid(row=0, column=1, sticky='NSEW')
    log.config(yscrollcommand=scrollbar.set)

    # makes the log resize with the window width
    log.bind('<Configure>', lambda e: log.configure(width=round(root.winfo_width() / 40)))

    # calling a callback function that subscribes the log to a mqtt topic
    callback(log)
