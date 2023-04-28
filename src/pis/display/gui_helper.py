from tkinter import Label, Toplevel, Canvas, TclError

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
        self.update_idletasks()

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



class ToastMessage(Toplevel):
    """
    Display toast messages in tkinter GUI. Toasts stack at bottom left corner.

    Attributes:
        instances (list): List of all the instances of ToastMessage.
        toastlevel (int): A counter to track the number of active toasts.

    Args:
        parent: The parent window for the toast message. Root Window recommended.
        message (str): The message to be displayed in the toast.
        duration (int, optional): The duration of the toast in milliseconds. Default is 3000.
        bg (str, optional): The background color of the toast. Default is '#323232'.
        fg (str, optional): The foreground color of the toast. Default is '#ffffff'.
        font (tuple, optional): The font of the toast. Default is ('Helvetica', 12).

    Methods:

        show(self):
            Displays the toast message with a default background.

        warn(self):
            Displays the toast message with a yellow background.

        error(self):
            Displays the toast message with a red background.

        success(self):
            Displays the toast message with a green background.
    """
    
    instances = []
    toastlevel = 1
    
    def __init__(self, parent, message, duration=3000, bg='#323232', fg='#ffffff', font=('Helvetica', 12)):
        super().__init__(parent)
        self.attributes('-type', 'splash')
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.withdraw()
        
        self.bg = bg
        self.fg = fg
        self.font = font
        self.duration = duration
        
        self.message = Label(self, text=message, bg=bg, fg=fg, font=font)
        self.message.pack(pady=(10, 10), padx=10, expand=True)
        self.message.configure(wraplength=parent.winfo_width(), anchor='w')
        self.prev_y = parent.winfo_y() + parent.winfo_height()
        
        self.bindID = parent.bind("<Configure>", self.update_position,  add="+")
       
       
    def show(self):
        self.deiconify()
        self.update_idletasks()
        
         # Get the position of the master window
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty() + (self.master.winfo_height() - self.winfo_height() * ToastMessage.toastlevel)
        self.Y = (self.master.winfo_y() + self.master.winfo_height()) - y 
    
        self.geometry("+{}+{}".format(x, y))
        self.update()
        self.attributes('-alpha', 0.0)
        self.fade_in()
        self.master.after(self.duration, self.fade_out)
        
    
    def update_position(self, event):
        if event.widget == self.master:
            try:
                x = self.master.winfo_x()
                y = (int(event.y) + int(event.height)) - int(self.Y)
                self.geometry('+%d+%d' % (x, y))
                self.update()
            except TclError:
                pass
        
    def warn(self):
        ''' yellow color setup'''
        self.configure(bg="#FFC107")
        self.message.configure(bg="#FFC107", fg="#333333")
        self.show()
        
    def error(self):
        ''' red color setup'''
        self.configure(bg="#F44336")
        self.message.configure(bg="#F44336", fg="#FFFFFF")
        self.show()
        
    def success(self):
        ''' green color setup'''
        self.configure(bg="#4CAF50")
        self.message.configure(bg="#4CAF50", fg="#FFFFFF")
        self.show()
        
        
    def fade_in(self):
        ToastMessage.toastlevel += 1
        ToastMessage.instances.append(self)
        
        start_x = self.master.winfo_rootx() - self.winfo_width()
        stop_x = self.master.winfo_rootx()
        distance = start_x - stop_x
        
        for i in range(20):
            progress = (i + 1) / 20
            x_new = start_x - distance * progress
            self.geometry("+{}+{}".format(int(x_new), (int(int(self.master.winfo_y())) + int(self.master.winfo_height())) - int(self.Y)))
            self.update_idletasks()
        
        
    def fade_out(self):     
        self.master.unbind("<Configure>", self.bindID)
        ToastMessage.instances.remove(self)
        ToastMessage.toastlevel -= 1
        self.destroy()
        for instance in ToastMessage.instances:
            self.Y = instance.winfo_y() + instance.winfo_height()
            instance.geometry('+%d+%d' % (instance.master.winfo_x(), self.Y))
            instance.update()


class VerticalScrollText(Canvas):
    """Scroll text vertically in a canvas when text overflows the canvas height"""
    def __init__(self, parent, text, fg, bg, justify, offsetx=0, offsety=0, speed=100, font=('Calibri Light', 15)):
        """
        Args:
            parent (tk.Root): A parent widget
            text (str): string or label to be displayed
            width (int, optional): width of widget and overflow limit. Defaults to 400.
            height (int, optional): height of widget and overflow limit. Defaults to 200.
            offsetx (int, optional): text offset position x coord. Defaults to 0.
            offsety (int, optional): text offset position y coord. Defaults to 0.
            speed (int, optional): Scrolling speed, smaller is faster. Defaults to 50.
        """
        super().__init__(parent, bg=bg, highlightthickness=0)
        self.update_idletasks()
        self.h = int(self.cget("height"))
        self.x = offsetx
        self.y = offsety
        self.speed = speed
        self.parent = parent
        self._animate = True
        
        
        
        self.text = self.create_text(offsetx, self.h+offsety, anchor="nw", text=text, font=font, fill=fg, justify=justify)
        #self.overflow_check()
        
    def overflow_check(self):
        cheight = int(self.cget("height"))
        bbox = self.bbox(self.text)
        th = bbox[3] - bbox[1]
        
        #on overflow animate scrolling
        if th > cheight:
            self._animate = True
            self.scroll_text()   
        else:
            if self._animate:
                self._animate = False
                self.move(self.text, 0, -cheight) 
        
    def scroll_text(self):
        self.move(self.text, 0, -1) 
        canvas_y = self.coords(self.text)[1] 
        if self.bbox(self.text)[3] == 0:  
            self.move(self.text, 0, self.h + self.y + abs(canvas_y))  # Move the text back to the bottom of the canvas
        self.parent.after(self.speed, self.scroll_text)
        
        
    def update_text(self, new_text):
        self.itemconfigure(self.text, text=new_text)
        
        self.overflow_check()
        
        
    def resize_font(self, font):
        self.itemconfigure(self.text, font=font)
        
        