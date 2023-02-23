from tkinter import Label


def configureGrid(d_type, frame, grid):
    rows = 11
    if d_type == 'MAIN':
        columns = 4
    elif d_type == 'PLATFORM':
        columns = 3
    else:
        return

    while rows >= 0:
        grid.rowconfigure(frame, rows, weight=1)
        rows = rows - 1
    while columns >= 0:
        grid.columnconfigure(frame, columns, weight=1)
        columns = columns - 1


def fillGrid(d_type, frame):
    rows = 10
    Label(frame, text="Time", font=('Calibri Light', 16), bg="white").grid(row=0, column=0, sticky="NSEW")
    Label(frame, text="Notice", font=('Calibri Light', 16), bg="white").grid(row=0, column=1, sticky="NSEW")

    if d_type == 'MAIN':
        columns = 4
        Label(frame, text="Platform", font=('Calibri Light', 16), bg="white").grid(row=0, column=2, sticky="NSEW")
        Label(frame, text="Train", font=('Calibri Light', 16), bg="white").grid(row=0, column=3, sticky="NSEW")
        Label(frame, text="Destination", font=('Calibri Light', 16), bg="white").grid(row=0, column=4, sticky="NSEW")
    elif d_type == 'PLATFORM':
        columns = 3
        Label(frame, text="Train", font=('Calibri Light', 16), bg="white").grid(row=0, column=2, sticky="NSEW")
        Label(frame, text="Destination", font=('Calibri Light', 16), bg="white").grid(row=0, column=3, sticky="NSEW")
    else:
        return

    labels = []
    r = 1
    while r <= rows:
        c = 0
        while c <= columns:
            color = '#2788c2'
            if (r % 2) == 0:
                color = '#36a8eb'
            l = Label(frame, text="", bg=color, fg='white', font=('Consolas', 15))
            l.grid(row=r, column=c, sticky="NSEW")
            labels.append(l)
            c += 1
        r += 1
    return labels
