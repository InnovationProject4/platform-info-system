from Event import Event, Observer, MutationObserver, Reactive
from collections import UserList



class ObservableList(list, MutationObserver):
    def __init__(self, *args, **kwargs):
        MutationObserver.__init__(self)
        list.__init__(self, *args, **kwargs)
        
		
    def __setitem__(self, index, value):
        old = self[index]
        list.__setitem__(self, index, value)
        self.events.notify("update", index, old, value)

    def append(self, value):
        index = len(self)
        list.append(self, value
        self.events.notify('append', index, [value])
