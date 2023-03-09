from abc import ABC, abstractmethod
import table_printer as printer


# Abstact class for different kinds of displays
class Display(ABC):

    @abstractmethod
    def printDisplay(self, msg):
        pass

    @abstractmethod
    def getTopic(self):
        pass

    @abstractmethod
    def getType(self):
        pass

    def printWarning(self, msg):
        printer.printWarningOnDisplay(msg.payload.decode())
        pass

    def printNotification(self, msg):
        printer.printNotificationOnDisplay(msg.payload.decode())
        pass


# Provides information about all trains arriving at the station (departing time, possible delay, platform, train number, destination)
class StationMainDisplay(Display):

    def __init__(self, station):
        self.station = station

    def printDisplay(self, msg):
        try:
            printer.printMainDisplay(msg.payload.decode())
        except:
            print("Error printing display")
            pass

    def getTopic(self):
        return f"station/{self.station}/main"

    def getType(self):
        return "MAIN"


# Provides information about the next 10 trains arriving to the platform (departing time, possible delay, train number, destination)
class PlatformDisplay(Display):

    def __init__(self, station, platform_number):
        self.platform_number = platform_number
        self.station = station

    def printDisplay(self, msg):
        try:
            printer.printPlatformDisplay(msg.payload.decode())
        except:
            print("Error printing display")
            pass

    def printPassingTrain(self, msg):
        try:
            printer.printPassingTrainOnDisplay(msg.payload.decode())
        except:
            print("Error printing passing train")
            pass

    def getTopic(self):
        return [f"station/{self.station}/{self.platform_number}"]

    def getType(self):
        return "PLATFORM"


class DualPlatformDisplay(Display):

    def __init__(self, station, platform_number1, platform_number2):
        self.platform_number1 = platform_number1
        self.platform_number2 = platform_number2
        self.station = station

    def printDisplay(self, msg):
        if msg.topic == self.getTopic()[0]:
            self.printLeft(msg)
        elif msg.topic == self.getTopic()[1]:
            self.printRight(msg)

    def printRight(self, msg):
        try:
            printer.printRightDisplay(msg.payload.decode())
        except:
            print("Error printing display")
            pass

    def printLeft(self, msg):
        try:
            printer.printLeftDisplay(msg.payload.decode())
        except:
            print("Error printing display")
            pass

    def getTopic(self):
        return [f"station/{self.station}/{self.platform_number1}",
                f"station/{self.station}/{self.platform_number2}"]

    def getType(self):
        return "DUAL_PLATFORM"
