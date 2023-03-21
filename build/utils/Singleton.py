import threading
import sqlite3

class Singleton:
    ''' A thread-safe approach to singletons '''

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None: 
            with cls._lock:
                # Another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._connection = sqlite3.connect(':memory:', check_same_thread=False)
                    print("invoked")
        return cls._instance

'''
Unit-test
'''
def test_singleton_is_always_same_object():
    assert Singleton() is Singleton()

    # Sanity check - a non-singleton class should create two separate
    #  instances
    class NonSingleton:
        pass
    assert NonSingleton() is not NonSingleton()