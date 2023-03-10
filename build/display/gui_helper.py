from tkinter import Label, Frame


def configureGrid(frame, grid, rows, columnlabels):
    columns = len(columnlabels) - 1
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
    for r in range(1, rows+1):
        for c in range(len(columnlabels)):
            color = '#2788c2'
            if (r % 2) == 0:
                color = '#36a8eb'
            label = Label(frame, text="", bg=color, fg='white', font=('Calibri Light', 15))
            label.grid(row=r, column=c, sticky="NSEW")
            labels.append(label)
    return labels


def configureDualPlatformGrid(frame, grid, fillside):
    for rows in range(4):
        grid.rowconfigure(frame, rows, weight=1)
    grid.columnconfigure(frame, 0, weight=1)

    labels = []
    color = '#36a8eb'
    for i in range(4):
        l = Label(frame, text="", fg="white", bg=color, font=('Calibri Light', 10))
        labels.append(l)

    fillside(labels)
    return labels


def fillLeftSide(labels):
    for i, l in enumerate(labels):
        l.grid(row=i, column=0, sticky="W", padx=(20, 0))


def fillRightSide(labels):
    for i, l in enumerate(labels):
        l.grid(row=i, column=1, sticky="E", padx=(0, 20))
