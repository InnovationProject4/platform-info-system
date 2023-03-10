''''
    Decorator based flyweight Observable pattern.
'''
import os
os.environ['PATH'] = 'export PATH=\"/usr/local/opt/tcl-tk/bin:\$PATH\""'
os.environ['TCL_LIBRARY'] = '/usr/local/Cellar/tcl-tk/8.6.13_1'
os.environ['TK_LIBRARY'] = '/usr/local/Cellar/tcl-tk/8.6.13_1'
import tkinter as tk
import weakref

class Event(object):
    __slots__ = ("callbacks")
    def __init__(self):
        self.callbacks = weakref.WeakSet()

    def notify(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)

    def register(self, callback):
        self.callbacks.add(callback)
        return callback



class EventBootstrap(object):
    __slots__ = ('__dict__')
       
    def attach(self, prop):
        setattr(self, prop, Event())

    def detach(self, prop):
        slot = getattr(prop)
        del slot


class Observable:
    __slots__ = ("events")
    def __init__(self):
        self._events = {}

    def attachEvent(self, prop):
        if prop not in self._events:
            self._events[prop] = Event()

    def detachEvent(self, prop):
        event = getattr(prop)
        del event



def observe(obj):
    if callable(obj):
        ''' is unbound function '''
        event = Event()
        def unboundWrapperGetter(*args, **kwargs):
            result = obj(*args, **kwargs)
            event.notify(obj, obj.__name__, result)
            return result
        
        unboundWrapperGetter.event = event

        return unboundWrapperGetter
    elif not obj:
         raise TypeError("Please specify an attribute or a method to observe.")

    'is attribute key'
    attr_key = obj
    value_key = '_%s' % attr_key


    def attr_getter(object):
        return getattr(object, value_key)

    def attr_setter(object, value):
        setattr(object, value_key, value)
        object._events[attr_key].notify(object, attr_key, value)

    def boundWrapperGetter(*args, **kwargs):
            value = prop(*args, **kwargs)
            args[0]._events[key].notify(prop, key, value)
            return value

    def attribute_decorator(prop):
        if isinstance(prop, type):
            '''is class'''
            cls = prop

        else: raise TypeError("Please specify an observable class.")

        if hasattr(cls, attr_key) and callable(getattr(cls, attr_key)):
            '''attribute is method'''
            setattr(cls, value_key, property(fget=boundWrapperGetter))
            return cls

        '''attribute is value'''
        setattr(cls, value_key, property(fget=attr_getter, fset=attr_setter))
        return cls

    return attribute_decorator

        


def observable(attr_key):
    if not attr_key:
        raise TypeError("Please specify an attribute to observe.")

    value_key = '_%s' % attr_key 
    event_key = '_%s_eventListener' % attr_key

    def getter(obj):
        return getattr(obj, value_key)

    def setter(obj, value):
        event = getattr(obj, event_key)
        setattr(obj, value_key, value)
        event.notify(obj, attr_key, value)

    def classWrapper(cls):
        instance = cls.__init__
        def __init__(self, *args, **kwargs):
            setattr(self, event_key, Event())
            instance(self,*args,**kwargs)

        setattr(cls, attr_key, property(fget=getter, fset=setter))
        setattr(cls, '__init__', __init__)
        return cls

    return classWrapper

'''
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



