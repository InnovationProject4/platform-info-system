# Platform information system  
  
#### ✨Developed at Metropolia's innovation project course for a client at Nokia.✨  
  
 By. Leevi Laaksonen, Samuel Laisaar, Leo Lehtiö, Aleksandr Liski  
The goal of this project is to develop a train station display board system. The system provides the possibility to handle multiple displays at various different train stations. These could be for example the main display that shows information of all trains departing at the station and displays on individual platforms.  
  
## Architecture  
  
The system retrieves rail traffic information from Digitraffic's services and uses MQTT protocol to distribute the information to different topics which the displays at railway stations subscribe. In the displays implementation the data is then formatted and displayed in a GUI. 
  
![data flow diagram](doc/diagrams/data_flow_diagram.png)  
  
### MQTT topic naming convention  
Topic for train data
```sh  
station/<station-short-code>/<platform-number>/<transit>/<transport-type>
```  

> Transit: **DEPARTURE** or **ARRIVAL** 
> Transport type: **Commuter** or **Long-distance**

> **Outputs a JSON string:**  {train: [trainNumber, trainType, trainCategory, commuterLineID, timetable: [type, cancelled, scheduledTime, differenceInMinutes, liveEstimateTime, commercialTrack, cause]]}  
>

Topic for non stopping trains at a platform  
```sh  
station/<station-short-code>/<platform-number>/passing  
```  
> **Outputs a JSON string:** > {station, trains: [track, scheduledTime]}  
>   
Topic for all announcements in a station
```sh  
announcements/<notify-type>/<station-code>/<platform-id>
```  

> Notify type: **info**, **alert** or **infoview** 

Topic for device communication
```sh  
management/<display-id>/update
```  
> Subtopic **"update"** not mandatory and is used only for notifying the aggrigator to publish data from a database
## Installation  
  
For running the build on Linux  
  
Install Eclipse Mosquitto  
```sh  
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa  
sudo apt-get update  
sudo apt-get install mosquitto  
sudo apt-get install mosquitto-clients  
```  
Start the broker  
```sh  
mosquitto  
```  
  
Clone the repository with git  
```sh  
git clone https://github.com/InnovationProject4/platform-info-system  
```  
Navigate to the "build" folder.  
  
You will need to install the requirements.txt files:  
```sh  
pip3 install -r requirements.txt  
```  
  
Edit the config.ini file to change the ip and port of the mqtt broker.
Also specify what station you want the server to aggregate.
```sh  
[mqtt-broker]  
ip = localhost  
port = 1883  

[aggregation]
target_station=PSL
```  
### Server  
  
The server can be executed with the command:  
```sh  
python3 server.py 
```  
### Displays  
  
The display can be executed with the command:  
```sh  
python3 display_client.py -view <display_view> -s <station_short_code> -p <platform> -left <platform> -right <platform> -transit<transit> -transport<transport>  
```  
> Here is an explanation of the different parameters:\  
> -view "tableview" requires the parameters -s, -transit and -transport but -p is optional\  
> -view "splitview" requires parameters -s, -left, -right, -transit and -transport\  
> -view "platformview" requires parameters -s , -p, -transit and -transport\  
> -view "infoview" requires the parameter -s  
  
### Manager  
  
The manager can be executed with the command:  
```sh  
python3 manager_client.py  
```
