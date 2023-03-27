import tkinter as tk
from tkinter import ttk

from utils.tkui import Viewport
from messaging.telemetry import Connection
from utils.Event import Reactive

import math, time, datetime, configparser




config = configparser.ConfigParser()
config.read('config.ini')
ADDR = config.get('mqtt-broker', 'ip')
PORT = config.getint('mqtt-broker', 'port')


conn = Connection(ADDR, 1883)


attached=None

class DeviceMonitoring(Viewport, ):
    '''
    Attaches to Management Node and monitors displays
    '''
    
    #plugin
    name = "Display monitor"
    
    @staticmethod
    def default(parent):
       plugin = DeviceMonitoring(parent)
       return plugin
   
    def __init__(self, parent, width=100, height=100, *args, **kwargs):
        super().__init__(parent, bg="red",width=width, height=height, *args, **kwargs)
        
        self.displays = {}
        
       
        self.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)
        self.widgets()
        
        attached.event.register(self.parse_display_data)
        
        
    def parse_display_data(self, name, result, *args):
        now = datetime.datetime.now()
        dt_pre = now - datetime.timedelta(minutes=10)
        dt_post = now + datetime.timedelta(minutes=10)
        
        self.treeview.delete(*self.treeview.get_children())
        
        
        for display in result:
            last_message = display[3]
            first_message = display[4]
            status = display[5]
            
            last_message = datetime.datetime.fromtimestamp(last_message).replace(microsecond=0)
            first_message = datetime.datetime.fromtimestamp(first_message).replace(microsecond=0)
            
            if not dt_pre <= last_message <= dt_post:
                status = "untrusted"
            
            tuple =  display[:3] + (last_message, first_message, status)
            
            self.treeview.insert('', tk.END, text='', values=tuple, tags=(status,))
        
        if result:
            self.autoscale(self.treeview)
            
        
    
    
    
    def widgets(self):
        
        device_list_frame = tk.Frame(self)
        device_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # create device list treeview
        device_list_treeview = ttk.Treeview(device_list_frame)
        device_list_treeview.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)
        
        device_list_treeview['columns'] = ('uuid', 'name', 'type', 'last_msg', 'first_conn', 'status')
        device_list_treeview.column('#0', width=0, stretch=tk.NO)
        device_list_treeview.column('uuid', width=100, anchor=tk.CENTER)
        device_list_treeview.column('name',  width=100, anchor=tk.CENTER)
        device_list_treeview.column('type',  width=100, anchor=tk.CENTER)
        device_list_treeview.column('last_msg', width=150, anchor=tk.CENTER)
        device_list_treeview.column('first_conn', width=150, anchor=tk.CENTER)
        device_list_treeview.column('status', width=100, anchor=tk.CENTER)
        
        #add headings to treeview
        device_list_treeview.heading('uuid', text='UUID')
        device_list_treeview.heading('name', text='Display Name')
        device_list_treeview.heading('type', text='Type')
        device_list_treeview.heading('last_msg', text='Last message')
        device_list_treeview.heading('first_conn', text='First Contact')
        device_list_treeview.heading('status', text='Status')
        
        #self.autoscale(device_list_treeview, fontSize=12)
        
        
        # configure tags for device status
        device_list_treeview.tag_configure('connected', background='#8bc34a')
        device_list_treeview.tag_configure('disconnected',  foreground="#333", background='#9e9e9e')
        device_list_treeview.tag_configure('untrusted',  foreground="#000", background='#FFDC00')
        
        self.treeview = device_list_treeview
 
 
    
    @staticmethod
    def attach(func):
        global attached
        attached = func
        
        
        
    def destroy(self):
        self.pack_forget()
        
        



#############################################################


#############################################################

class MessageRateGauge(Viewport):
    '''
    Monitor message rate per minute
    '''

    # plugin
    name = "Message Rate Gauge"

    @staticmethod
    def default(parent):
        return MessageRateGauge(parent)

    def __init__(self, parent, width=200, height=200, *args, **kwargs):
        super().__init__(parent, bg="red", width=width, height=height, *args, **kwargs)

        self.message_rate = Reactive(0)
        self.last_minute_count = 0
        self.message_count = 0

        # draw gauge when rate data is changed
        self.message_rate.watch(self.draw)

        # message rate gauge
        self.max_rate = 1000
        self.needle_len = min(width, height) // 2 * 0.8
        self.needle_width = min(width, height) // 20

        conn.on_connection(self.on_connect)
        if not conn.is_connected():
            conn.connect()        
        

        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.place(relx=0.5, rely=0.5, anchor="center")

        # start a timer to update message rate every minute
        self.after(60000, self.update_message_rate)

        self.draw()

    def on_connect(self):
        conn.subscribe("$SYS/broker/messages/received", lambda client, userdata, message: (
            self.aggregate(message.payload.decode())
        ))

    def aggregate(self, payload):
        if self.message_count == 0:
            self.message_count = self.last_minute_count = int(payload)
        else:
            self.message_count = int(payload)

    def update_message_rate(self):
        # calculate message rate per minute
        self.message_rate.value = self.message_count - self.last_minute_count
        self.last_minute_count = self.message_count

        self.after(60000, self.update_message_rate)

    def draw(self):
        self.canvas.delete("all")

        # draw gauge background
        cx = self.canvas.winfo_width() // 2
        cy = self.canvas.winfo_height() // 2
        r = min(cx, cy) * 0.9
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#ddd", width=2)

        # draw gauge scale
        for i in range(0, self.max_rate+1, 100):
            angle = -135 + 270 * i / self.max_rate
            x1 = cx + (r-2) * math.cos(math.radians(angle))
            y1 = cy + (r-2) * math.sin(math.radians(angle))
            x2 = cx + (r-10) * math.cos(math.radians(angle))
            y2 = cy + (r-10) * math.sin(math.radians(angle))
            self.canvas.create_line(x1, y1, x2, y2, width=2)

        # draw gauge needle
        rate = self.message_rate.value
        angle = -135 + 270 * rate / self.max_rate
        x1 = cx
        y1 = cy
        x2 = cx + self.needle_len * math.cos(math.radians(angle))
        y2 = cy + self.needle_len * math.sin(math.radians(angle))
        self.canvas.create_line(x1, y1, x2, y2, width=self.needle_width, fill="red")

        # draw gauge value
        self.canvas.create_text(cx, cy, text="{:.2f} msg/min".format(rate), font=("Arial", 12, "bold"))

        # schedule next draw
        self.after(1000, self.draw)