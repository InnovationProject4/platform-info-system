import tkinter as tk
from dashboard import controller


def createDisplayLog(root, right_frame):
    status_log = tk.Text(right_frame, bg='#141414', fg='white', highlightthickness=0, borderwidth=0,
                         font=('Calibri Light', 13))
    status_log.configure(state="disabled")
    status_log.grid(row=0, column=0, sticky='NSEW', padx=(20, 20), pady=(20, 20))
    scrollbar = tk.Scrollbar(right_frame, command=status_log.yview)
    scrollbar.grid(row=0, column=1, sticky='NSEW')
    status_log.config(yscrollcommand=scrollbar.set)
    status_log.bind('<Configure>', lambda e: status_log.configure(width=round(root.winfo_width() / 40)))
    controller.connectToDisplays(status_log)
