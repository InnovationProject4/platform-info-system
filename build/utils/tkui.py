import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkFont
import sys, json, os.path

'''
A  window framework for TKinter that allow users to build custom views. 

View hierarchy is as follows:

    App - Is the root of the window. App may contain multiple worksspaces
    Workspace - is the root document for views.
    ViewGroup - Arranges viewports in different layouts
    Viewport  - Represents a view. Plugin inherited.
    
    App
        - Workspace "Monitoring"
            - ViewGroup1
                Viewport1
                Viewport2
            - ViewGroup2
                Viewport3
                Viewport4
                
        - Workspace "Connectivity"
            - ViewGroup3
                -Viewport5

note: App may mount only one Workspace at a time.
note: App will create a default workspace which will create a default ViewGroup

Example usage:
if __name__ == "__main__":
    # creates default Workspace
    app = App()
    
    # Render hierarchy
    deviceGroup = ViewGroup(app.workspace, description="shitgroup", orient=tk.VERTICAL, bg="black")
    devicelist = Template(deviceGroup, "telemetry", bg="red")
    message_vp = Viewport(deviceGroup, "messaging", bg="green")
    
    # Layout hierarchy
    app.add_viewgroup(deviceGroup)
    deviceGroup.add_viewports([message_vp, devicelist])
    
    app.run()
'''

__all__ = (
    "Viewport",
    "ViewGroup",
    "Workspace",
    "App"
)


class App(tk.Tk):
    '''
    constructor will create a default workspace which will createa a default ViewGroup
    '''
    def __init__(self, width=1024, height=768, workspace=None, plugins=None, title="Dashboard"):
        super().__init__()
        self.geometry(f"{width}x{height}")
        self.minsize(800,600)
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.propagate(False)
        self.title(title)
        self.workspace = workspace or self.load_default() or Workspace(self)
        self.workspace.pack(fill=tk.BOTH, expand=True)
        self.spaces = [self.workspace]
        self.plugins = plugins if plugins else []
        
        self.bind_selector_menu()
        #self.bind("<ButtonRelease-1>", get_focused_item) # Debugging mouse presses
        self.bind("<ButtonRelease-3>", self.show_menu)
        

        
    def add_viewgroup(self, viewgroup):
        self.workspace.add_viewgroup(viewgroup)
        return viewgroup
    
    def remove_viewgroup(self, viewgroup):
        self.workplace.remove_viewgroup(viewgroup)
        
    def add_workspace(self, workspace):
        self.spaces.append(workspace)
        self.update_spaces_menu()
        
    def remove_workspace(self, workspace):
        if self.workspace == workspace:
            workspace.pack_forget()
            
        self.spaces.remove(workspace)
        
    def use_workspace(self, workspace):
        ''' App may only mount one workspace at a time. The currently active workspace will be unmounted (hidden) and replaced '''
        if self.workspace:
            self.workspace.pack_forget()
            self.forget(self.workspace)
        
        workspace.pack(fill=tk.BOTH, expand=True)
        for vg in workspace.view_groups:
            vg.pack(fill=tk.BOTH, expand=True)
            
        self.workspace = workspace
        
    def use_next_workspace(self):
        ''' rotates through workspaces on call'''
        self.counter += 1 % len(self.spaces)
        
        if self.workspace and self.spaces:
            self.workspace.pack_forget()
            self.workspace = self.workspaces[self.counter]
            self.workspace.pack(fill=tk.BOTH, expand=True)
            
            
    def load_default(self, wspace=None):
        '''Attempt to load default workspace file if exists in home directory'''
        if wspace is None:
            return self.load_default("default.wspace")
        
        try:
            with open(wspace, "r") as f:
                return JSONDeserializer.deserialize(json.loads(f.read()), self)

        except FileNotFoundError:
            print("error")
            pass
            
            
    def save_config(self):
        ''' Save current workspace to File'''
        with tk.filedialog.asksaveasfile(defaultextension=".wspace") as file:
            if file is not None:
                
                ws = self.workspace.serialize()
                ws["params"]["description"] = os.path.basename(file.name)
                
                file.write(json.dumps(ws))
                file.close()
    
    
        
    
    def load_config(self):
        ''' Load a workspace from File '''
        file = filedialog.askopenfilename(initialdir='', title='Select a workspace', filetypes=[('Workspaces', '.wspace')])
        ws = self.load_default(file)
        
        if isinstance(ws, Workspace):
            self.spaces.append(ws)
            self.update_spaces_menu()
    
    
    def update_spaces_menu(self):
        # ADD WORKSPACES TO WORKSPACE MENU, DISABLE ACTIVE CONTEXT
        
        spaces_menu = self.menu.nametowidget(self.menu.entrycget("Use Workspace", "menu"))
        spaces_menu.delete(0, "end")
        
        # ADD WORKSPACES TO WORKSPACE MENU, DISABLE ACTIVE CONTEXT
        #TODO: thes eare useles change to either add_command or switch to something else
        for ws in self.spaces:
            var = tk.BooleanVar()
            var.set(True)
            
            spaces_menu.add_checkbutton(label=ws.description, variable=var, command=lambda ws=ws:{
                ws.pack(fill=tk.BOTH, expand=True),
                self.use_workspace(ws)
                
            })
            
            ws.update()
        self.update()
        
        
    def bind_selector_menu(self):
        '''
        Context menu for right-click on viewports
        '''
        self.menu = tk.Menu(self, tearoff=0)
        layout_menu = tk.Menu(self.menu, tearoff=0)
        plugin_menu = tk.Menu(self.menu, tearoff=0)
        spaces_menu = tk.Menu(self.menu, tearoff=0)
        
        # LAYOUT MENU
        layout_menu.add_command(label="Split View", command=lambda: (
            vg := self.workspace.active_viewgroup,
            vg.split_viewport() 
        ))
        
        layout_menu.add_separator()
        layout_menu.add_command(label="Split In Horizontal Group", command=lambda: (
            vg := self.workspace.active_viewgroup,
            vg.split_in_group(vg.active_viewport, "horizontal"),
        ))
        
        layout_menu.add_command(label="Split In Vertical Group", command=lambda: (
            vg := self.workspace.active_viewgroup,
            vg.split_in_group(vg.active_viewport, "vertical")
        ))
        
        # PLUGIN MENU  
        for plugin in self.plugins:
            plugin_menu.add_command(label=plugin.name, command=lambda plugin=plugin: (
                vg := self.workspace.active_viewgroup,
                vg.swap_viewports(vg.active_viewport, plugin.default(vg)),
                self.update()
            ))
        
   
        self.menu.add_cascade(label="Layout", menu=layout_menu)
        self.menu.add_cascade(label="Plugin", menu=plugin_menu)
        self.menu.add_separator()
        self.menu.add_command(label="Save Workspace As...", command=self.save_config)
        self.menu.add_command(label="Load Workspace from File...", command=self.load_config)
        self.menu.add_separator()
        self.menu.add_cascade(label="Use Workspace", menu=spaces_menu)
        self.menu.add_separator()
        self.menu.add_command(label="Close", command=lambda : (
            vg := self.workspace.active_viewgroup,
            vp := vg.active_viewport,
            vg.remove_viewport(vp),
            vp.destroy()
        ))
        
        # ADD WORKSPACES TO WORKSPACE MENU, DISABLE ACTIVE CONTEXT
        self.update_spaces_menu()
        
        
    def show_menu(self, event):
        element = traverse_search(event.widget, Viewport)
        parent = element.parent
        parent.set_active_viewport(element)
        self.workspace.set_active_viewgroup(parent)
        
        self.menu.post(event.x_root, event.y_root)
        
    def onClose(self):
        self.quit()
        
    
    def run(self):
        self.mainloop()
        
        
        
        
class Workspace(tk.Canvas):
    '''
    Workspace: Represents the entire app, which can contain multiple view groups. 
    It can also include references to additional settings, such as the active view group and the current workspace directory.
    '''
    def __init__(self, parent, description="Default Persona"):
        super().__init__(parent)
        self.parent = parent
        self.description = description
        self.active_viewgroup = None
        self.view_groups = []
        
        self.configure(bg='lightgray')
        
    def serialize(self):
        children = []
        for child in self.winfo_children():
            if hasattr(child, 'serialize'):
                children.append(child.serialize())
                
        return {
            '__parent__':self.parent.__class__.__name__,
            '__class__': "Workspace",
            '__children__': children,
            "params": {
                "description": self.description
            },
            "attributes": {
                #"view_groups": [vg.serialize() for vg in self.view_groups]
            }
        }
        
        
        
    def set_active_viewgroup(self, viewgroup):
        self.active_viewgroup = viewgroup
        
    def add_viewgroup(self, view_group):
        view_group.pack(fill=tk.BOTH, expand=True)
        self.active_viewgroup = view_group
        self.view_groups.append(view_group)
        
    def remove_viewgroup(self, view_group):
        view_group.forget(self)
        self.forget(view_group)
        self.view_groups.remove(view_group)



class ViewGroup(ttk.PanedWindow):
    def __init__(self, parent, description="Default Group", viewports=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.description = description
        self.viewports = viewports or []
        self.active_viewport = self.viewports[0] if self.viewports else None
        self.isroot = isinstance(self.parent, Workspace)

        
        if viewports:
            for viewport in self.viewports:
                self.add(viewport)
                
    
    def serialize(self):
        children = []
        panes = []
        
        ''' split view, but I don't know why panes are empty sometimes, so adding also self.viewports below'''
        for child in self.panes():
            if hasattr(child, 'serialize'):
                panes.append(child.serialize())
                
        childs = {}
        
        '''split in group'''
        #for child in self.winfo_children():
        #    if hasattr(child, 'serialize'):
        #        children.append(child.serialize())
        
        def x(a):
            childs[id(a)] = a.serialize()
        
        ''' split view'''
        [x(child) for child in self.viewports if hasattr(child, 'serialize')]
        '''split in group'''
        [x(child) for child in self.winfo_children() if hasattr(child, 'serialize')]
        
        for child in childs.values():
            children.append(child)
        

        return {
            '__parent__':self.parent.__class__.__name__,
            '__class__': self.__class__.__name__,
            '__panes__': panes,
            '__children__': children,
            '__sashes__' : [self.sashpos(i) for i in range(len(self.panes()) - 1)],
            "params": {
                "description": self.description
            },
            "attributes": {
                #"viewports": [vp.serialize() for vp in self.viewports],
                "orient" : str(self["orient"])
            }
        }
                
    def unattach(self):
        self.parent.remove_viewgroup(self)
        self.pack_forget()
        self.forget(self.parent)
        self.parent = None
        
    def set_active_viewport(self, viewport):
        self.active_viewport = viewport
                
                
    def add_viewport(self, viewport):
        self.add(viewport)
        self.viewports.append(viewport)
        self.active_viewport = viewport
        
    def add_viewports(self, viewports):
        for viewport in viewports:
            self.viewports.append(viewport)
            self.add(viewport)
            
        self.active_viewport = viewports[0]
        
    def remove_viewport(self, viewport):
        self.viewports.remove(viewport)
        self.forget(viewport)
        
        #empty group
        if not self.viewports:
            self.unattach()
            self.destroy()
        
        
    
    def remove_viewgroup(self, view_group):
        self.remove_viewport(view_group)
        
        
    def swap_viewports(self, removable, addable):
        idx = self.panes().index(str(removable))
        
        self.insert(idx, addable) # Render hierarchy
        self.viewports.append(addable) # Layout hierarchy
        self.active_viewport = addable
        addable.parent = self
        removable.unattach()
            
        
        
    def split_in_group(self, viewport, orient="vertical"):
        '''
        You can split a viewport into a new group, creating a new view group and moving the current viewport to it.
        '''
        viewport.unattach()
    
        new_group = ViewGroup(self, orient=orient)
        viewport.parent = new_group
    
        self.viewports.append(new_group)
        self.add(new_group)
        self.active_viewport = viewport

        new_group.add_viewport(viewport)
        new_group.add_viewport(Viewport(new_group, ""))
        
        
    def split_viewport(self):
        temp_viewport = Viewport(self, "default viewport")
        self.add_viewport(temp_viewport)
            
            
     
         
        
class Viewport(tk.Frame):
    '''
    Viewport: Represents a single window displays a specific view. 
    It can contain a reference to a specific file or document, and can be associated with view-related settings.
    '''
    
    def __init__(self, parent, *args, **kwargs):
        '''kwarghs are used so it's easier for deserializer to initialize'''
        super().__init__(width=kwargs["width"], height=kwargs["height"], bg=kwargs["bg"], highlightcolor="#525252", highlightthickness=1, highlightbackground="#4d4d4d", relief=tk.SUNKEN)
        self.parent = parent 
        self.description = kwargs["description"]
        self.width = kwargs["width"]
        self.height = kwargs["height"]
        
    def __init__(self, parent, description="Default Viewport", width=200, height=200, bg="gray"):
        super().__init__(width=width, height=height, bg=bg, highlightcolor="#525252", highlightthickness=1, highlightbackground="#4d4d4d", relief=tk.SUNKEN)
        self.parent = parent
        self.description = description
        self.width = width
        self.height = height
        
        
        self.style = ttk.Style(self)
        
        
    def serialize(self):
        return {
            '__parent__':self.parent.__class__.__name__,
            '__class__': self.__class__.__name__,
            "params": {
                "description": self.description
            },
            "attributes": {
                "test_id": "test-id-234j209j-23498rujw"
            }
        }
    
    def unattach(self):
        self.pack_forget()
        self.parent.remove_viewgroup(self)
        self.parent = None
        
    def remove(self):
        self.pack_forget()
        
    def autoscale(self, tree, fontSize=10, minSize=8, maxSize=14):
        ''' make text content in some widgets responsive '''
        # fontSize = scaling factor heuristic
        
        def __autoscale_treeview(event):
            ''' scale text in TreeView '''
            if event.widget == self: return
            
            # Get the smaller dimension of the widget
            smallest_dimension = min(event.width, event.height)
            
            # Calculate the new font size based on the smaller dimension
            new_font_size = max(min(smallest_dimension // fontSize, maxSize), minSize) 
            
            # "take first row to check for content overflow" hack
            items = tree.item(tree.get_children()[0], option="values")
            
            rid = 0
            for column in tree['columns']:
                cell_width = tree.column(column, width=None)
                cell_text = tree.heading(column, "text")
                cell_font = tkFont.Font(family="TkDefaultFont", size=new_font_size)
                
                item_text = items[rid]
                text_width = max(cell_font.measure(cell_text),cell_font.measure(item_text))
                
                if text_width > cell_width:
                    new_font_size = max(int(new_font_size * (cell_width / text_width)), minSize)
                    
                rid += 1
                
            # Set the new font size for the Treeview and Treeview.Heading styles
            #style = ttk.Style()
            self.style.configure("Treeview", font=(None, new_font_size - 1))
            self.style.configure("Treeview.Heading", font=(None, new_font_size, "bold"))
        
        if tree.bind('<Configure>') == '':
            tree.bind('<Configure>', __autoscale_treeview)
        

### HELPERS ############################################################################################# 
        
def debug_get_focused_item(event):
    print("event widget:", event.widget)
    
    print("parent", event.widget.parent)
    
    

def traverse_search(widget, cls):
    ''' traverse and search on widget graph '''
    current = widget
    while current is not None:
        if isinstance(current, cls): return current
        current = current.master if current.master is not None else current.parent
    
    
    
    
class JSONDeserializer:
    ''' Deserialize Json format into tkui objects'''
    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return JSONDeserializer.deserialize(data)

    @staticmethod
    def deserialize(data, parent=None):
        if isinstance(data, dict):
            if '__class__' in data:
                class_name = data.pop('__class__')
                
                module = None
                for name, obj in sys.modules.items():
                    if hasattr(obj, class_name):
                        module = obj
                        break

                if module is None:
                    raise ImportError(f"Could not find module for class {class_name}")
                        
                cls = getattr(module, class_name) if module else globals()[class_name]
                args = {k: JSONDeserializer.deserialize(v, parent) for k, v in data.pop('params', {}).items()}
                instance = cls(parent, **args)
    
                for k, v in data.pop('attributes', {}).items():
                    setattr(instance, k, JSONDeserializer.deserialize(v, instance))
                for child in data.pop('__children__', []):
                    child_obj = JSONDeserializer.deserialize(child, instance)
                    #instance.add_child(child_obj)
                    
                    if isinstance(instance, Workspace):
                        instance.add_viewgroup(child_obj)
                        
                    elif isinstance(instance, ViewGroup):
                        instance.add_viewport(child_obj)
                    else:
                        raise TypeError("Instance is unknown type", type(instance))
                    
                    
                    
                for pane in data.pop('__panes__', []):
                    print("INSTPANE", instance, "CHILD", pane)
                    # split in group
                    pane_obj = JSONDeserializer.deserialize(pane, instance)
                    #instance.add_pane(pane_obj)
                    if isinstance(instance, Workspace):
                        instance.add_viewgroup(pane_obj)
                        
                    elif isinstance(instance, ViewGroup):
                        instance.add_viewport(pane_obj)
                    else:
                        raise TypeError("Instance is unknown type", type(instance))
                    
        
                sashpos = data.pop('__sashes__', [])
                if sashpos:
                    i = 0
                    for pos in sashpos:
                        instance.sashpos(i, pos)
                        i = i + 1
                        
                
                
                
                    
                #setattr(instance, 'sashes', data.pop('__sashes__', []))
                return instance
            else:
                return {k: JSONDeserializer.deserialize(v, parent) for k, v in data.items()}
        elif isinstance(data, list):
            return [JSONDeserializer.deserialize(item, parent) for item in data]
        else:
            return data
    

class Template(Viewport):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        device_list_frame = tk.Frame(self)
        device_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # create device list treeview
        device_list_treeview = ttk.Treeview(device_list_frame)
        device_list_treeview.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)
        
        device_list_treeview['columns'] = ('uuid', 'name', 'last_msg', 'last_conn', 'status')
        device_list_treeview.column('#0', width=0, stretch=tk.NO)
        device_list_treeview.column('uuid', width=100, anchor=tk.CENTER)
        device_list_treeview.column('name',  width=100, anchor=tk.CENTER)
        device_list_treeview.column('last_msg', width=150, anchor=tk.CENTER)
        device_list_treeview.column('last_conn', width=150, anchor=tk.CENTER)
        device_list_treeview.column('status', width=100, anchor=tk.CENTER)
        
        #add headings to treeview
        device_list_treeview.heading('uuid', text='UUID')
        device_list_treeview.heading('name', text='Device Name')
        device_list_treeview.heading('last_msg', text='Last message')
        device_list_treeview.heading('last_conn', text='Last contact')
        device_list_treeview.heading('status', text='Status')
        


'''
if __name__ == "__main__":
    # creates default Workspace and default viewgroup
    app = App()
    
    # Render hierarchy
    deviceGroup = ViewGroup(app.workspace, description="shitgroup", orient=tk.VERTICAL, bg="black")
    devicelist = Template(deviceGroup, "telemetry", bg="red")
    message_vp = Viewport(deviceGroup, "messaging", bg="green")
    
    
    
    # Layout hierarchy
    app.add_viewgroup(deviceGroup)
    deviceGroup.add_viewports([message_vp, devicelist])
    
    app.run()
'''