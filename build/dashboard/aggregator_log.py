import tkinter as tk
from dashboard import controller


def createAggregatorLog(root, middle_frame):
    aggregator_log = tk.Text(middle_frame, bg='#141414', fg='white', highlightthickness=0, borderwidth=0,
                         font=('Calibri Light', 13))
    aggregator_log.configure(state="disabled")
    aggregator_log.grid(row=0, column=0, sticky='NSEW', padx=(20, 20), pady=(20, 20))
    scrollbar = tk.Scrollbar(middle_frame, command=aggregator_log.yview)
    scrollbar.grid(row=0, column=1, sticky='NSEW')
    aggregator_log.config(yscrollcommand=scrollbar.set)
    aggregator_log.bind('<Configure>', lambda e: aggregator_log.configure(width=round(root.winfo_width() / 40)))
    controller.connectToAggregator(aggregator_log)
