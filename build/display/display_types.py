from abc import ABC, abstractmethod
import display.display_printer as printer


# Abstact class for different kinds of displays
class Display(ABC):

    @abstractmethod
    def handleSubscriptions(self):
        pass


class TableCentralDisplay(Display):

    def __init__(self, station):
        self.station = station

    def handleSubscriptions(self):
        return [
            (f"station/{self.station}/main", lambda client, userdata, message: (
                printer.printTableCentralDisplay(message.payload.decode())
            )),
            (f"station/{self.station}/warning", lambda client, userdata, message: (
                printer.printWarningOnDisplay(message.payload.decode())
            )),
            (f"announcement/alert/{self.station}", lambda client, userdata, message: (
                printer.printAnnouncementsOnDisplay(message.payload.decode())
            )),
        ]


class TablePlatformDisplay(Display):

    def __init__(self, station, platform_number):
        self.platform_number = platform_number
        self.station = station

    def handleSubscriptions(self):
        return [
            (f"station/{self.station}/{self.platform_number}", lambda client, userdata, message: (
                printer.printTablePlatformDisplay(message.payload.decode())
            )),
            (f"station/{self.station}/warning", lambda client, userdata, message: (
                printer.printWarningOnDisplay(message.payload.decode())
            )),
            (f"announcement/+/{self.station}/{self.platform_number}", lambda client, userdata, message: (
                printer.printAnnouncementsOnDisplay(message.payload.decode())
            )),
            (f"station/{self.station}/{self.platform_number}/passing", lambda client, userdata, message: (
                printer.printPassingTrainOnDisplay(message.payload.decode())
            )),
        ]


class DualPlatformDisplay(Display):

    def __init__(self, station, platform_number1, platform_number2):
        self.platform_number1 = platform_number1
        self.platform_number2 = platform_number2
        self.station = station

    def handleSubscriptions(self):
        return [
            (f"station/{self.station}/{self.platform_number1}", lambda client, userdata, message: (
                printer.printLeftDisplay(message.payload.decode())
            )),
            (f"station/{self.station}/{self.platform_number2}", lambda client, userdata, message: (
                printer.printRightDisplay(message.payload.decode())
            )),
            (f"station/{self.station}/warning", lambda client, userdata, message: (
                printer.printWarningOnDisplay(message.payload.decode())
            ))
        ]
