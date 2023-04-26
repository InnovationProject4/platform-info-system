import tkinter as tk
from tkinter import ttk

from pis.utils.tkui import Viewport
from pis.messaging.telemetry import Connection
from pis.utils.Event import Reactive

import pis.utils.conf as conf
import math, time, datetime, configparser


conf.Conf()

conn = Connection(conf.ADDR, 1883)


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
        
        label = PluginLabel(self, "hello world")
        label.pack()
        
        
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
        
        


class PluginLabel(tk.Frame):
    def __init__(self, parent, plugin_name, plugin_description="KEK"):
        super().__init__(parent)
        
        self.plugin_name = plugin_name
        self.plugin_description = plugin_description
        
        self.label_name = tk.Label(self, text=self.plugin_name, font=("Arial", 14))
        self.label_description = tk.Label(self, text=self.plugin_description, font=("Arial", 10), wraplength=200)
        
        self.label_name.pack(side=tk.TOP)
        self.label_description.pack(side=tk.BOTTOM)