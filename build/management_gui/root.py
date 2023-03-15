import tkinter as tk
from management_gui import display_log, server_log, announcement_manager, infodisplay_manager


def createRoot():
    root = tk.Tk()
    root.geometry("1280x720")
    root.title("")

    # Configures the amount of columns and rows for root
    tk.Grid.columnconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 1, weight=1)
    tk.Grid.columnconfigure(root, 2, weight=1)
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.rowconfigure(root, 1, weight=60)

    # Adding labels to top of the root
    tk.Label(root, text="Announcement manager", font=('Calibri Light', 15)).grid(row=0, column=0, sticky='NSEW')
    tk.Label(root, text="Server log", font=('Calibri Light', 15)).grid(row=0, column=1, sticky='NSEW')
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

    display_log.createDisplayLog(root, right_frame)

    server_log.createServerLog(root, middle_frame)

    announcement_manager.createAnnouncementManager(left_frame)

    infodisplay_manager.createInfodisplayManager(left_frame, root)

    return root


