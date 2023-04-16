from tkinter import Label, Toplevel, Canvas

# Configures the grid of a tableview
def configureGrid(frame, grid, rows, columnlabels):
    columns = len(columnlabels) - 1
    rows += 1
    while rows >= 0:
        grid.rowconfigure(frame, rows, weight=1)
        rows = rows - 1
    while columns >= 0:
        grid.columnconfigure(frame, columns, weight=1)
        columns = columns - 1


# Fills the tableview's grid with labels and returns them
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


# Configures the splitview's grid and creates labels for them
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


# Adds labels to the left frame of splitview
def fillLeftSide(labels):
    for i, l in enumerate(labels):
        l.grid(row=i, column=0, sticky="W", padx=(20, 0))


# Adds labels to the right frame of splitview
def fillRightSide(labels):
    for i, l in enumerate(labels):
        l.grid(row=i, column=1, sticky="E", padx=(0, 20))


def showWarning(main_frame, warning_frame, warnings):
    if len(warnings) > 0 and warnings[0] != '':
        warning_frame.tkraise()
    else:
        main_frame.tkraise()


def updateLabels(reactive, label):
    label.config(text=reactive)


# Usíng predefined font sizes to resize labels
# Callback is view's resizeFonts method
def checkResize(root, resize_fonts_callback):
    w = root.winfo_width()
    h = root.winfo_height()
    if w > 1500 and h > 500:
        resize_fonts_callback({"sm": 30, "md": 35, "lg": 40, "xl": 60, "xxl": 80})
        return
    elif w > 1000 and h > 500:
        resize_fonts_callback({"sm": 20, "md": 25, "lg": 30, "xl": 50, "xxl": 65})
        return
    elif w > 600 and h > 500:
        resize_fonts_callback({"sm": 15, "md": 20, "lg": 25, "xl": 48, "xxl": 55})
        return
    elif w > 300 and h > 200:
        resize_fonts_callback({"sm": 10, "md": 15, "lg": 20, "xl": 40, "xxl": 45})
        return


def changeNotification(notification_id, notification_label, notifications):
    if notification_id >= len(notifications):
        notification_id = 0
    if len(notifications) > 0:
        notification_label.config(text=notifications[notification_id])
    notification_id += 1
    # Returns an id of the next notification
    return notification_id


class SplashTriangle(Toplevel):
    '''
    example of a triangle splash screen usage

    root = tk.Tk()
    root.geometry('800x600')

    splash = SplashTriangle(root, 'Varokaa ohittavaa Junaa', "Beware of the passing train", "Se upp för täget som passerar stationen")
    splash.show(15000)

    root.mainloop()
    '''

    def __init__(self, parent, *messages):
        super().__init__(parent)
        # self.attributes('-type', 'splash')
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.withdraw()

        self.geometry('+%d+%d' % (parent.winfo_x(), parent.winfo_y()))
        self.update_idletasks()

        pw = parent.winfo_width()
        ph = parent.winfo_height()

        ''' canvas relative size and anchor to parent
            default width expected 600
            default height expected 400
        '''
        rsize = int((pw / 600) * 250)
        padding = 80
        xpos = pw - rsize - padding
        ypos = ph - rsize - padding

        # top corner
        x1 = rsize // 2 + xpos
        y1 = ypos

        # left corner
        x2 = xpos
        y2 = rsize + ypos

        # right corder
        x3 = rsize + xpos
        y3 = rsize + ypos

        self.canvas = Canvas(self, width=pw, height=ph, bg='#00008b')
        self.canvas.pack()
        self.triangle = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="yellow", outline="red", width=15)

        dy = 50
        for message in messages:
            text = self.canvas.create_text(50, dy, width=450, text=message, anchor="nw",
                                           font=("Helvetica", self.resize_font(pw), "bold"), fill="white")
            dy += self.canvas.bbox(text)[3] - self.canvas.bbox(text)[1] + 40

    def resize_font(self, width):
        return int((width / 600) * 12)

    def hide(self):
        self.withdraw()

    def show(self, duration):
        self.deiconify()
        self.after(duration, self.hide)
        self.update_idletasks()
