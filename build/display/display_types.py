from abc import ABC, abstractmethod
import display.display_printer as printer


# Abstract class for different kinds of displays
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
                printer.addTrains(message.payload.decode(), {"station": self.station, "transit": self.transit, "transport": self.transport, "view": "tableview"})
            )),
            (f"announcement/alert/{self.station}", lambda client, userdata, message: (
                printer.printWarningOnDisplay(message.payload.decode())
            )),
            (f"announcement/info/{self.station}", lambda client, userdata, message: (
                printer.printAnnouncementsOnDisplay(message.payload.decode())
            ))]


class Platform(Display):

    def __init__(self, station, platform_number, transit, transport, view):
        self.platform_number = platform_number
        self.station = station
        self.transit = transit
        self.transport = transport
        self.view = view

    def handleSubscriptions(self):
        return [
            (f"station/{self.station}/{self.platform_number}/{self.transit}/{self.transport}",
             lambda client, userdata, message: (
                 printer.addTrains(message.payload.decode(), {"platform": self.platform_number, "transit": self.transit, "transport": self.transport, "view": self.view})
             )),
            (f"announcement/alert/{self.station}/{self.platform_number}", lambda client, userdata, message: (
                printer.printWarningOnDisplay(message.payload.decode())
            )),
            (f"announcement/info/{self.station}/{self.platform_number}", lambda client, userdata, message: (
                printer.printAnnouncementsOnDisplay(message.payload.decode())
            )),
            (f"station/{self.station}/{self.platform_number}/passing", lambda client, userdata, message: (
                printer.printPassingTrainOnDisplay(message.payload.decode())
            ))]


class DualPlatform(Display):

    def __init__(self, station, platform_number1, platform_number2, transit, transport):
        self.platform_number1 = platform_number1
        self.platform_number2 = platform_number2
        self.station = station
        self.transit = transit
        self.transport = transport

    def handleSubscriptions(self):
        return [
            (f"station/{self.station}/{self.platform_number1}/{self.transit}/{self.transport}",
             lambda client, userdata, message: (
                 printer.addTrains(message.payload.decode(), {"view": "splitview"})
             )),
            (f"station/{self.station}/{self.platform_number2}/{self.transit}/{self.transport}",
             lambda client, userdata, message: (
                 printer.addTrains2(message.payload.decode())
             )),
            (f"announcement/alert/{self.station}", lambda client, userdata, message: (
                printer.printWarningOnDisplay(message.payload.decode())
            )),
            (f"announcement/info/{self.station}", lambda client, userdata, message: (
                printer.printAnnouncementsOnDisplay(message.payload.decode())
            ))]


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
            ))]
