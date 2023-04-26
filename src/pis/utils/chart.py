
import tkinter as tk


class Line():
   def __init__(self, *args,parent=None ,color="blue" ,height=1):
      chart = parent if parent else args[0]

      self.line_color = color
      self.line_height = height
      self.y_end = 0
      self.x_end  = chart.line_len*-1
      self.values = []
      
   
   def configure(self , color=None ,height=None) :
      if color != None:
         self.line_color = color
      if height != None:
         self.line_height = height
         
def getActualWidth(text="" ,font=None):
    label = tk.Label(font=font)
    label.config(text=str(text) +"      ")
    return label.winfo_reqwidth()


class LineChart:
    def __init__(self, *args, parent=None, width=None, height=None, sections=None, vbar_size=None, hbar_size=None, 
                  bg=None, fg=None, hbar_fg=None, vbar_fg=None, sections_fg=None, text_color=None, font=None, 
                  labels=None, max_value=None, line_len=None, sections_count=10, labels_count=10,
                  top=10, bottom=10, left=10, right=10, x=40, y=40):
        
        self.master = parent if parent else args[0]
        
        self._width = width 
        self._height = height
        
        self.sections = sections
        self.labels = labels
    
        self.vbar_size = vbar_size
        self.hbar_size = hbar_size
        
        self.sections_fg = sections_fg,
        self._bg = bg
        self._fg = fg 
        self.hbar_fg = hbar_fg 
        self.vbar_fg = vbar_fg
        
        self.font = font
        self.text_color = text_color 
        self.max_value = max_value
        self.line_len = line_len
        
        self.left = getActualWidth(text=max_value ,font=font) + left
        self.right = right
        self.top = top
        self.bottom = bottom 
        
        self.sections_count = sections_count
        self.labels_count = labels_count
        
        self._x = x
        self._y = y
        
        self.display_lines = []
        
        self.backframe = tk.Frame(parent)
        self.label_frame = tk.Frame(self.backframe)
        self.label_1 = tk.Label(self.backframe, width=right, fg=text_color, font=font, bg=bg)
        self.label_n = tk.Label(self.backframe, width=right, fg=text_color, font=font, bg=bg)
        self.vbar = tk.Frame(self.backframe)
        self.hbar = tk.Frame(self.backframe)
        self.canvas_bg = tk.Frame(self.backframe)
        self.canvas = tk.Canvas(self.canvas_bg, highlightthickness=0)
        
        self.update_geometry()
        self.update_colors()
        
        if self.sections: self.update_sections()
        if self.labels: self.update_labels()
        
        
        def __autoscale(e):
            print(e.width, e.height)
            self._width = e.width
            self._height = e.height
            
            #self.reset_canvas()
            self.delete_sections()
            self.delete_labels()
            self.update_sections()
            self.update_labels()
            self.update_geometry()
            
            
        
        self.backframe.bind("<Configure>", __autoscale)
        
        
    def reset(self):
        self.display_lines = []
        self.reset_canvas()
        
        
    def update_geometry(self):
        labely = self.top + self._y + self.hbar_size
        w = self._width - (self.left+self.vbar_size+self._x+self.right)
        h = self._height - (self.hbar_size * 2 + self.top + self._y + self.bottom)
        vbarh = self._height-(self.top+self.bottom)
        hbarw = self._width-(self.left+self.right)
        
        self.backframe.configure(width=self._width, height=self._height)
        self.label_frame.place(width=self.left, y=labely, height=h)
        self.vbar.place(width=self.vbar_size, x=self.left, y=self.top, height=vbarh)
        self.hbar.place(height=self.hbar_size, x=self.left, y=self._height-self.bottom-self.hbar_size, width=hbarw)
        self.canvas_bg.place(x=self.left+self.vbar_size,y=self.top+self._y+self.hbar_size, width=w, height=h)
        self.canvas.place(x=0, y=0, width=self._width-5-(self.left+self.vbar_size+self._x+self.right), height=h)
        
        self.rerender()
        
                
    def update_sections(self):
        y = 0
        for n in range(self.sections_count + 1):
            tk.Frame(self.canvas_bg, height=1, bg=self.sections_fg).place(relwidth=1, width=-5, y=y)
            y = (self._height - (self.hbar_size * 2 + self.top + self._y + self.bottom)) / self.sections_count * n
            
            
    def delete_sections(self):
        for w in self.canvas_bg.winfo_children():
            if type(w) == tk.Frame:
                w.destroy()
                
    
    def delete_labels(self):
        self.label_1.place_forget()
        for w in self.label_frame.winfo_children():
            if type(w) == tk.Label:
                w.destroy()
        
        self.label_n.place_forget()
        
    
    def update_labels(self):
        self.label_1.config(anchor='e', text=str(round(self.max_value+0.0, 1))+" ", bg=self._bg, fg=self.text_color, font=self.font)
        self.label_1.place(y=self.top+self._y+self.hbar_size, width=self.left, anchor='w')
        
        for n in range(1, self.labels_count):
            text = round(self.max_value / self.labels_count * (self.labels_count - n), 1)
            y = (self._height - (self.hbar_size * 2 + self.top + self._y + self.bottom)) / self.labels_count * n
            tk.Label(self.label_frame, anchor='e', text=str(text)+" ", bg=self._bg, fg=self.text_color, font=self.font).place(y=y, anchor="w", width=self.left)
            
        self.label_n.config(anchor="e", text=str(0.0)+" ", fg=self.text_color, font=self.font, bg=self._bg)
        self.label_n.place(y=self._height-self.bottom-self.hbar_size, anchor="w", width=self.left)
      
        
    def update_colors(self):
        self.backframe.configure(fg_color=self._bg)
        self.label_frame.configure(fg_color=self._bg)
        self.vbar.configure(bg=self.vbar_fg)
        self.hbar.configure(bg=self.hbar_fg)
        self.canvas_bg.configure(bg=self._fg)
        self.canvas.configure(bg=self._fg)
        
       
             
    
    def configure(self, **kwargs):
        reset_chart = False
        reset_size = False 
        reset_labels = False
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
        if kwargs["font"] != None or kwargs["max_value"] != None:
            reset_size = True
            reset_chart = True 
            reset_labels = True
        
                
        if kwargs["left"] != None:
            self.left = self.left + getActualWidth(text=self.max_value, font=self.font)
            reset_chart = True
        else:
            if reset_size:
                self.left = self.left - getActualWidth(text=self.max_value, font=self.font)
                if kwargs["font"] != None or kwargs["max_value"] != None:
                    self.left = self.left + getActualWidth(text=self.max_value, font=self.font)
                    
        if reset_labels:
            self.delete_labels()
            if self.sections == True or kwargs["sections"] == True:
                self.update_sections()
            
        
        if reset_chart:
            self.update_geometry()
            
            
    def reset_canvas(self):
        self.chart_x = 0
        self.chart_width = self._width - 5 - (self.left + self.vbar_size + self._x + self.right)
        self.chart_height = self._height - (self.hbar_size * 2 + self.top + self._y + self.bottom)
        self.canvas.place(x=0, y=0, width=self.chart_width, height=self.chart_height)
        
        self.canvas.delete("all")
        
    def rerender(self):
        self.reset_canvas()
        
        if(len(self.display_lines) > 0):
            index = int( ((self.chart_width) / self.line_len) - ((self.chart_width / self.line_len) * 2) )
            
            max_values = len (self.display_lines[0].values)
            
            for line in self.display_lines:
                if max_values < len(line.values): max_values = len(line.values)
                
            for line in self.display_lines:
                line.values += [None for x in range(max_values - len(line.values))]
                line.values = line.values[index:]
                
            for line in self.display_lines:
                while None in line.values : 
                    line.values.remove(None)
                    
            tmp = self.display_lines
            self.display_lines = []
            
            for line in tmp:
                line.x_end = self.line_len*- 1
                line.y_end = 0
                tmp_val = line.values
                line.values = []
                if len(tmp_val) != 0:
                    self.render(values=tmp_val, line=line)

        
        
    def render(self, line=None, values=None):
        if line not in self.display_lines:
            self.display_lines.append(line)
            
        line.values += values
        x_start = line.x_end
        y_start = line.y_end
        
        for value in values:
            line.x_end += self.line_len
            line.y_end = (self.chart_height - (self.chart_height/100) * (value / self.max_value * 100) + (line.line_height / 2))
            self.canvas.create_line(x_start, y_start, line.x_end, line.y_end, fill=line.line_color, width=line.line_height)
            
            if line.x_end > self.chart_width:
                self.chart_x -= self.line_len
                self.chart_width += self.line_len
                if self.chart_width > self._width * 2: 
                    self.rerender()
                else:
                    self.canvas.place(x = self.chart_x, y=0, width=self.chart_width, height=self._height-(self.hbar_size * 2 + self.top + self._y + self.bottom))
            
            x_start = line.x_end
            y_start = line.y_end
          
            
    def place(self, x=None, y=None, rely=None, relx=None, anchor=None):
        self.backframe.place(x=x, y=y, rely=rely, relx=relx, anchor=anchor)
        
    def pack(self, x=None, y=None, pady=None, padx=None, before=None, expand=None, fill=None, after=None, side=None, ipadx=None, ipady=None, anchor=None):
        self.backframe.pack(x=x, y=y, pady=pady, padx=padx, before=before, expand=expand, fill=fill, after=after, side=side, ipadx=ipadx, ipady=ipady, anchor=anchor)
        
    def grid(self, column=None, columnspan=None, ipadx=None, ipady=None, padx=None, pady=None, row=None, rowspan=None, sticky=None):
        self.backframe.grid(column=column, columnspan=columnspan, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady, row=row, rowspan=rowspan, sticky=sticky)