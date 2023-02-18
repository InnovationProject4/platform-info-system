from abc import ABC, abstractmethod
import table_printer as printer

# Abstact class for different kinds of displays
class Display(ABC):

    @abstractmethod
    def printDisplay(self, msg):
        pass

    @abstractmethod
    def getTopic(self, station):
        pass


# Provides information about all trains arriving at the station (departing time, possible delay, platform, train number, destination)
class StationMainDisplay(Display):

    def printDisplay(self, msg):
        try:
            printer.printMainDisplay(msg)
        except:
            pass


    def getTopic(self, station):
        return f"station/{station}/main"

# Provides information about the next 10 trains arriving to the platform (departing time, possible delay, train number, destination)
class PlatformDisplay(Display):

    def __init__(self, platform_number):
        self.platform_number = platform_number

    def printDisplay(self, msg):
        try:
            printer.printPlatformDisplay(msg)
        except:
            pass

    def getTopic(self, station):
        return f"station/{station}/{self.platform_number}"