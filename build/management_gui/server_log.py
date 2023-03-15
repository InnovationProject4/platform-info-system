import tkinter as tk


def createServerLog(root, middle_frame):
    server_log = tk.Text(middle_frame, bg='#141414', fg='white', highlightthickness=0, borderwidth=0,
                         font=('Calibri Light', 13))
    server_log.configure(state="disabled")
    server_log.grid(row=0, column=0, sticky='NSEW', padx=(20, 20), pady=(20, 20))
    scrollbar = tk.Scrollbar(middle_frame, command=server_log.yview)
    scrollbar.grid(row=0, column=1, sticky='NSEW')
    server_log.config(yscrollcommand=scrollbar.set)
    server_log.bind('<Configure>', lambda e: server_log.configure(width=round(root.winfo_width() / 40)))
