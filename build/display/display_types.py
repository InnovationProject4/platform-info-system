from abc import ABC, abstractmethod
import display.display_printer as printer


# Abstact class for different kinds of displays
class Display(ABC):


    @abstractmethod
    def handleSubscriptions(self):
        pass


class Central(Display):

    def __init__(self, station, transit, transport):
        self.station = station
        self.transit = transit
        self.transport = transport

    def handleSubscriptions(self):
        return [
            (f"station/{self.station}/+/{self.transit}/{self.transport}", lambda client, userdata, message: (
                printer.addTrains(message.payload.decode(), f"{self.station} {self.transit}")
            )),
            (f"announcement/alert/{self.station}", lambda client, userdata, message: (
                printer.printWarningOnDisplay(message.payload.decode())
            )),
            (f"announcement/info/{self.station}", lambda client, userdata, message: (
                printer.printAnnouncementsOnDisplay(message.payload.decode())
            ))
        ]


class Platform(Display):

    def __init__(self, station, platform_number, transit, transport):
        self.platform_number = platform_number
        self.station = station
        self.transit = transit
        self.transport = transport

    def handleSubscriptions(self):
        return [
            (f"station/{self.station}/{self.platform_number}/{self.transit}/{self.transport}", lambda client, userdata, message: (
                printer.addTrains(message.payload.decode(), f"{self.platform_number} {self.transit}")
            )),
            (f"announcement/alert/{self.station}/{self.platform_number}", lambda client, userdata, message: (
                printer.printWarningOnDisplay(message.payload.decode())
            )),
            (f"announcement/info/{self.station}/{self.platform_number}", lambda client, userdata, message: (
                print(message.payload.decode()),
                printer.printAnnouncementsOnDisplay(message.payload.decode())
            )),
            (f"station/{self.station}/{self.platform_number}/passing", lambda client, userdata, message: (
                printer.printPassingTrainOnDisplay(message.payload.decode())
            ))
        ]


class DualPlatform(Display):

    def __init__(self, station, platform_number1, platform_number2, transit, transport):
        self.platform_number1 = platform_number1
        self.platform_number2 = platform_number2
        self.station = station
        self.transit = transit
        self.transport = transport

    def handleSubscriptions(self):
        return [
            (f"station/{self.station}/{self.platform_number1}/{self.transit}/{self.transport}", lambda client, userdata, message: (
                printer.addTrains(message.payload.decode(), "")
            )),
            (f"station/{self.station}/{self.platform_number2}/{self.transit}/{self.transport}", lambda client, userdata, message: (
                printer.addTrains2(message.payload.decode())
            )),
            (f"announcement/alert/{self.station}", lambda client, userdata, message: (
                printer.printWarningOnDisplay(message.payload.decode())
            )),
            (f"announcement/info/{self.station}", lambda client, userdata, message: (
                printer.printAnnouncementsOnDisplay(message.payload.decode())
            ))
        ]


class Information(Display):

    def __init__(self, station):
        self.station = station

    def handleSubscriptions(self):
        return [
            (f"announcement/infoview/{self.station}", lambda client, userdata, message: (
                printer.printAnnouncementsOnDisplay(message.payload.decode())
            )),
            (f"announcement/alert/{self.station}", lambda client, userdata, message: (
                printer.printWarningOnDisplay(message.payload.decode())
            ))
        ]
