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
    column_labels = []
    for i, label in enumerate(columnlabels):
        new_label = Label(frame, text=label, font=('Calibri Light', 16), bg="white")
        new_label.grid(row=0, column=i, sticky="NSEW")
        column_labels.append(new_label)

    train_labels = []
    for r in range(1, rows+1):
        for c in range(len(columnlabels)):
            color = '#061f36'
            if (r % 2) == 0:
                color = '#082743'
            label = Label(frame, text="", bg=color, fg='white', font=('Calibri Light', 15))
            label.grid(row=r, column=c, sticky="NSEW")
            train_labels.append(label)

    return train_labels, column_labels


def configureDualPlatformGrid(frame, grid, callback):
    for rows in range(4):
        grid.rowconfigure(frame, rows, weight=1)
    grid.columnconfigure(frame, 0, weight=1)

    labels = []
    color = '#082743'
    for i in range(4):
        l = Label(frame, text="", fg="white", bg=color, font=('Calibri Light', 10))
        labels.append(l)

    callback(labels)
    return labels


def fillLeftSide(labels):
    for i, l in enumerate(labels):
        l.grid(row=i, column=0, sticky="W", padx=(20, 0))


def fillRightSide(labels):
    for i, l in enumerate(labels):
        l.grid(row=i, column=1, sticky="E", padx=(0, 20))
