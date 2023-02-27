from tkinter import Label


def configureGrid(frame, grid, rows, columnlabels):
    columns = len(columnlabels)-1
    rows += 1
    while rows >= 0:
        grid.rowconfigure(frame, rows, weight=1)
        rows = rows - 1
    while columns >= 0:
        grid.columnconfigure(frame, columns, weight=1)
        columns = columns - 1


def fillGrid(frame, rows, columnlabels):
    for i, label in enumerate(columnlabels):
        Label(frame, text=label, font=('Calibri Light', 16), bg="white").grid(row=0, column=i, sticky="NSEW")

    labels = []
    r = 1
    while r <= rows:
        c = 0
        while c < (len(columnlabels)):
            color = '#2788c2'
            if (r % 2) == 0:
                color = '#36a8eb'
            l = Label(frame, text="", bg=color, fg='white', font=('Consolas', 15))
            l.grid(row=r, column=c, sticky="NSEW")
            labels.append(l)
            c += 1
        r += 1
    return labels
