from abc import ABC, abstractmethod
import display.display_printer as printer


# Abstact class for different kinds of displays
class Display(ABC):

    @abstractmethod
    def printDisplay(self, msg):
        pass

    @abstractmethod
    def getTopics(self):
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


class TableCentralDisplay(Display):

    def __init__(self, station):
        self.station = station

    def printDisplay(self, msg):
        try:
            printer.printTableCentralDisplay(msg.payload.decode())
        except:
            print("Error printing display")
            pass

    def getTopics(self):
        return [(f"station/{self.station}/main", 1),
                (f"station/{self.station}/warning", 1),
                (f"station/{self.station}/notification", 1)]

    def getType(self):
        return "MAIN"


class TablePlatformDisplay(Display):

    def __init__(self, station, platform_number):
        self.platform_number = platform_number
        self.station = station

    def printDisplay(self, msg):
        try:
            printer.printTablePlatformDisplay(msg.payload.decode())
        except:
            print("Error printing display")
            pass

    def printPassingTrain(self, msg):
        try:
            printer.printPassingTrainOnDisplay(msg.payload.decode())
        except:
            print("Error printing passing train")
            pass

    def getTopics(self):
        return [(f"station/{self.station}/{self.platform_number}", 1),
                (f"station/{self.station}/warning", 1),
                (f"station/{self.station}/notification", 1),
                (f"station/{self.station}/{self.platform_number}/passing", 1)]

    def getType(self):
        return "PLATFORM"


class DualPlatformDisplay(Display):

    def __init__(self, station, platform_number1, platform_number2):
        self.platform_number1 = platform_number1
        self.platform_number2 = platform_number2
        self.station = station

    def printDisplay(self, msg):
        if msg.topic == f"station/{self.station}/{self.platform_number1}":
            self.printLeft(msg)
        elif msg.topic == f"station/{self.station}/{self.platform_number2}":
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

    def getTopics(self):
        return [(f"station/{self.station}/{self.platform_number1}", 1),
                (f"station/{self.station}/{self.platform_number2}", 1),
                (f"station/{self.station}/warning", 1),
                (f"station/{self.station}/notification", 1)]

    def getType(self):
        return "DUAL_PLATFORM"
