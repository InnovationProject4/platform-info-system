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
Data for individual platform
```sh
station/<station-short-code>/<platform-number>
```

## Installation
For running the build locally on Linux

Install Eclipse Mosquitto  (with apt)
```sh
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
```
For running scripts you will need a Python module called paho-mqtt (with pip)
```sh
sudo pip install paho-mqtt
```

### Displays
Clone the repository with git
```sh
git clone https://github.com/InnovationProject4/platform-info-system
```
Navigate to the folder "build\display" and run the main python file
```sh
python3 main.py
```
