import tkinter as tk
from tkinter import ttk

from utils.tkui import Viewport
from messaging.telemetry import Connection
from utils.Event import Reactive

import utils.chart as chart

import time, math

#TODO : CONNECTION FACTORY AND ON CONNECT OBSERVER

conn = Connection("localhost", 1883)
conn.connect()
''''''
### Broker Message stats #######################################################################################################
class MessageStatsView(Viewport):
    '''
    Monitor brokers general behaviour.   brokerHealthMonitor, Client ConnectionLog BrokerStats, DebugLogs
    '''
    
    #plugin
    name = "Message Stats"
    
    @staticmethod
    def default(parent):
       plugin = MessageStatsView(parent)
       return plugin
        
    
    def __init__(self, parent, width=20, height=200, *args, **kwargs):
        super().__init__(parent, bg="red",width=width, height=height, *args, **kwargs)
        
        self.description = "Message Stats"
        
        self.messages_received = Reactive(0)
        self.messages_sent = Reactive(0)
        
        self.messages_sent_plot = []
        self.messages_received_plot = []
        
        
        # message rate gauge
        self.max_rate = 1000
        self.needle_len = min(width, height) // 2 * 0.8
        self.needle_width = min(width, height) // 20
        
        self.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)
        self.message_widgets()
        
        conn.on_connection(self.on_connect)
         
               
    def on_connect(self):
        conn.subscribe_multiple([
            
            ("$SYS/broker/messages/received", lambda client, userdata, message: (
                 self.received_aggregation(message.payload)
            )), 
            
            
            ("$SYS/broker/messages/sent", lambda client, userdata, message: (
                self.sent_aggregation(message.payload)
            ) )
            
        
          
             
        ])
        

    def received_aggregation(self, payload):
        num_messages = int(payload.decode())
        self.messages_received.value = num_messages
        
        now = time.time() // 60
        self.messages_received_plot.append((now, num_messages))
        
        # remove data points older than 60 minutes
        while len(self.messages_received_plot) > 0 and now - self.messages_received_plot[0][0] > 60:
            self.messages_received_plot.pop(0)
            
            
        self.received_line.set_data([d[0] for d in self.messages_received_plot], [d[1] for d in self.messages_received_plot])
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.canvas.draw()

        
    def sent_aggregation(self, payload):
        num_messages = int(payload.decode())
        self.messages_sent.value = num_messages
        
        now = time.time() // 60
        self.messages_sent_plot.append((now, num_messages))
        
        # remove data points older than 60 minutes
        while len(self.messages_sent_plot) > 0 and now - self.messages_sent_plot[0][0] > 60:
            self.messages_sent_plot.pop(0)
        

        self.sent_line.set_data([d[0] for d in self.messages_sent_plot], [d[1] for d in self.messages_sent_plot])
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.canvas.draw()
        
    
    def message_widgets(self):
        
        self.stats_label = tk.Label(self, text="Broker Statistics")
        self.stats_label.pack()
        
        received_label = tk.Label(self, text="Messages Received: ")
        received_label.pack()
        
        self.messages_received.watch(lambda: (
            received_label.configure(text="Messages Received: " + str(self.messages_received.value))
        ))
        
        sent_label = tk.Label(self, text="Messages Sent: ")
        sent_label.pack()
        
        self.messages_sent.watch(lambda: (
            sent_label.configure(text="Messages Sent: " + str(self.messages_sent.value))
        ))
        
        
        self.chart = chart.LineChart(
            self, width=600, height=400, hbar_size=5, vbar_size=5,
            hbar_fg="#101010", vbar_fg="#444444", sections_fg="#444444", 
            text_color="red", font=('arial', 8, 'bold'),
            sections=True, sections_count=10, max_value=100,
            labels=True, labels_count=10, line_len=20,
            left=10, right=10, bottom=40, top=40,
            x=0, y=0
        )
        
        self.chart.pack(fill=tk.BOTH, expand=True)
    
        
        return self
        
        
        
    def remove(self):
        self.pack_forget()
        
        
### Broker Message Rate Gauge #######################################################################################################
    
class MessageRateGauge(Viewport):
    '''
    Monitor message rate per minute
    '''
    
    #plugin
    name = "Message Rate Gauge"
    
    @staticmethod
    def default(parent):
        return MessageRateGauge(parent)
        
    
    def __init__(self, parent, width=200, height=200, *args, **kwargs):
        super().__init__(parent, bg="red",width=width, height=height, *args, **kwargs) 
    
        self.message_rate = Reactive(10)
        self.last_minute_count = 0
        self.message_count = None
        
        # draw gauge when rate data is changed
        self.message_rate.watch(self.draw)
    
        # message rate gauge
        self.max_rate = 1000
        self.needle_len = min(width, height) // 2 * 0.8
        self.needle_width = min(width, height) // 20
        
        
        conn.on_connection(self.on_connect)
        
        
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        
        # start a timer to update message rate every minute
        self.after(60000, self.update_message_rate)
        
        self.draw()
        
    
    def on_connect(self):
        conn.subscribe("$SYS/broker/publish/messages", lambda client, userdata, message: (
                self.aggregate(message.payload)
            ))
        
        
    def aggregate(self, payload):
        if self.message_count is None:
            self.message_count = self.last_minute_count = int(payload)
        else:
            self.message_count = int(payload)
        
        
        
        
    def update_message_rate(self):
        # calculate message rate per minute
        self.message_rate.value = self.message_count - self.last_minute_count
        self.last_minute_count = self.message_count
        
        self.after(60000, self.update_message_rate)
    
    
    def gauge(self):
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
        self.ax.set_theta_direction(-1)
        self.ax.set_theta_zero_location('N')
        self.ax.set_rlabel_position(0)
        self.ax.set_rlim(0, self.max_rate)
        self.ax.set_rticks(math.arange(0, self.max_rate+1, 100))
        self.ax.set_yticklabels([])
        self.ax.spines['polar'].set_visible(False)
        self.ax.grid(True)
        self.ax.set_title('Message Rate', fontweight='bold')
        
        self.needle = self.ax.plot([math.radians(-135)], [self.rate], color='red', linewidth=2)
        
      
    def draw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx = w // 2
        cy = h // 2
        r = min(w, h) // 2 * 0.9
        
        # draw gauge background
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
        
        
        
         
         
         
         
         
         
         
         
         
         
         
         
         
    