# Platform information system

#### ✨Developed at Metropolia's innovation project course for a client at Nokia.✨

    By. Leevi Laaksonen, Samuel Laisaar, Leo Lehtiö, Aleksandr Liski

The goal of this project is to develop a train station display board system. The system provides the possibility to handle multiple displays at various different train stations. These could be for example the main display that shows information of all trains departing at the station and displays on individual platforms.

## Architecture

The system retrieves rail traffic information from Digitraffic's services and uses MQTT protocol to distribute the information to different displays at railway stations.

![data flow diagram](doc/diagrams/data_flow_diagram.png)

### MQTT topic naming convention
Data for main display
```sh
station/<station-short-code>/main
```
> **Outputs a JSON string:** 
> {station , trains: [train, trainType, trainCategory, commuterID, time, actualTime, notice, platform, destination]}

Data for individual platform
```sh
station/<station-short-code>/<platform-number>
```
> **Outputs a JSON string:** 
> {platform, trains: [train, trainType, trainCategory, commuterID, time, actualTime, notice, platform, destination]}

Notification alert for individual station
```sh
station/<station-short-code>/notification
```
Warning alert for individual station
```sh
station/<station-short-code>/warning
```

## Installation

For running the build locally on Linux

Install Eclipse Mosquitto
```sh
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
```

### Displays

Clone the repository with git
```sh
git clone https://github.com/InnovationProject4/platform-info-system
```
You will need to install these following modules for running displays:
```sh
pip3 install paho-mqtt tabulate pytz
```
Navigate to the folder "build\display" and choose to run on console or with GUI

 Running in console:
 ```sh
python3 main.py --s <station-short-code> --t <display-type>
```
Running with Tkinter GUI:
```sh
python3 gui.py --s <station-short-code> --t <display-type>
```
The parameter "--s" means the station short code e.g "PSL" for Pasila station. The "--t" means what kind of display you want to inititate e.g "main" for the station main display or "1" for platform 1 display.
