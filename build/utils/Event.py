import weakref
from collections import UserDict

''' 
Contains several classes and functions related to obdservables and reactive values.
'''

__all__ = [
    'Event',
    'EventSet',
    'Observer',
    'Reactive',
    'MutationObserver',
    'observable'
]


class Event(object):
    def __init__(self):
        self.callbacks = set()

    def notify(self, *args, **kwargs):
        [callback(*args, **kwargs) for callback in self.callbacks]
        

    def register(self, callback):
        self.callbacks.add(callback)
        return callback


class EventSet(UserDict):
    def __missing__(self, key):
        self.data[key] = Event()
        return self.data[key]
    
    def __getattr__(self, key):
        event = self.get(key, None)
        if event is None: event = self.__missing__(key)
        return event



'''helper to create observable property on attribute'''
def observed_property(attr):
    key = '_%s' % attr

    def getter(obj):
        return getattr(obj, key)

    def setter(obj, value):
        old = obj.__dict__.get(key)
        setattr(obj, key, value)
        obj.events[attr].notify(attr, old, value)

    return property(fget=getter, fset=setter)

'''helper to create observable method'''
def observed_method(attr):
    key = attr.__name__
    def boundWrapperGetter(self, *args, **kwargs):
        result = attr(self, *args, **kwargs)
        self.events[key].notify(key, result)
        return result

    return boundWrapperGetter

'''
 Decorator function, which is used to turn class attributes into observables. It is to be used in combination with Observer and
 MutationObserver classes.
'''
def observable(*attributes):
    if callable(attributes[0]):
        ''' is unbound function '''
        event = Event()
        funct = attributes[0]
        def unboundWrapper(*args, **kwargs):
            result = funct(*args, **kwargs)
            event.notify(funct.__name__, result, *args)
            return result
        
        unboundWrapper.event = event
        return unboundWrapper

    ''' is attribute '''
    def decorator(cls):
        if not issubclass(cls, Observer): raise TypeError("Class must be a subclass of Observable.")

        for attr in attributes:
            if hasattr(cls, attr):
                prop = getattr(cls, attr)
                name = prop.__name__
                setattr(cls, name, observed_method(prop))
                
            else:
                key = '_%s' % attr
                setattr(cls, attr, observed_property(attr))
                
        return cls
    return decorator


'''
A base class for events. Must be used together with @observable decorator to function properly.

'''
class Observer:
    __slots__ = ('events')
    def __init__(self):
        self.events = EventSet()


'''
A reactive value that triggers updates when its value is changed.
It has a value property that can be set to trigger updates, and a watch method to register callbacks to be called on updates.

example usage:

counter = Reactive(0)   # 1. reactive value that is added to ButtonText

                        # 2. function that fires the event 'change'
def increment():
    counter.value = counter.value + 1

                        # 3.on update change button text to reactive value
self.button = ButtonText(self.root, text=counter)
reactive.watch(lambda : self.config(text=reactive.value))

                        # 4. When increment is invoked, reactive.watch launches to update button's self.config.text
                        #
'''
class Reactive:
    __slots__ = ("_value", "_watchers")
    def __init__(self, value):
        self._value = value
        self._watchers = set()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._notify()

    def _notify(self):
        for callback in self._watchers:
            callback()
                
    def watch(self, callback):
        self._watchers.add(callback)

    def unwatch(self, callback):
        self._watchers.discard(callback)


    def __str__(self):
        return f"Reactive({self._value})"



'''
A base class that provides an Event for subclasses to define a "mutation" event that fires when an attribute is set.
Subclasses may use __setattr__ or __setitem__ to trigger the mutation event.

example usage:

class Data(MutationObserver):
    def __init__(self, name):
        super().__init__()
        self.name = name

data = Data("container1")

@data.events.register
def test(key, old, value):
 print("key", key, value) 
'''
class MutationObserver:
    #__slots__ = ('_events')
    def __init__(self):
        self.events = Event()

    def __setattr__(self, key, value):
        old = self.__dict__.get(key)
        self.__dict__[key] = value
        self.events.notify(key, old, value)