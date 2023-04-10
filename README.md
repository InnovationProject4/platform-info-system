# Platform information system  
  
#### ✨Developed at Metropolia's innovation project course for a client at Nokia.✨  
  
 By. Leevi Laaksonen, Samuel Laisaar, Leo Lehtiö, Aleksandr Liski  
The goal of this project is to develop a train station display board system. 
 The system provides the possibility to handle multiple displays at various different train stations. 
 These displays can be, for example, a central display that shows information of all trains departing at the station and displays on individual platforms. 
 The displays can be configured with arguments to specify if, for example, the user wants to display only trains that are arriving and which are also commuter trains 
  
## Architecture  
  
The management node which is running the aggregator retrieves rail traffic data from Digitraffic's services and uses MQTT protocol to distribute the data to different topics which the displays at railway station's can subscribe. In the display's implementation the data is then validated, formatted and then displayed in with a GUI.

![data flow diagram](doc/diagrams/Sequence_diagram.png)  
  
> Sequence starts asynchronously from steps 1 to 2
> 1. Aggregator fetches data from Digitraffic.
> 2. Digitraffic responds with JSON data that is
   > filtered and published at step 5.
   > Since the operation is asynchronous,
   > data is published regardless whether any display is running.
> 
> From step 3 to 4, the display is selected to start
> 3. Display sends a ping event that includes a public key identifying itself for the Aggregator.
> 4. Aggregator sends an acknowledgment message with its public key.
> 5. Aggregator publishes the fetched train data to their corresponding topics.
> 6. Display verifies that the data has come from the aggregator and not from any external will. 
   > After that, the data is formatted into a form that the user interface can display
> 7. The User interface updates its view as it receives the formatted data.

### MQTT topic naming convention  
Topic for train data
```sh  
station/<station-short-code>/<platform-number>/<transit>/<transport-type>
```  

> Transit: **DEPARTURE** or **ARRIVAL** 
> Transport type: **Commuter** or **Long-distance**

> **Outputs a JSON string:**  [{stationFullName, schedule: [{Train:[trainNumber, trainType, trainCategory, commuterLineID, timetable: [destination, type, cancelled, scheduledTime, differenceInMinutes, liveEstimateTime, commercialTrack, trainStopping, cause, stops_on_stations:[]]]}]}]
>

Topic for non stopping trains at a platform  
```sh  
station/<station-short-code>/<platform-number>/passing  
```  
> **Outputs a JSON string:** > {station, trains: [track, scheduledTime]}  
>   
Topic for announcements in a station
```sh  
announcements/<notify-type>/<station-code>/<platform-id>
```  

> Notify type: **info**, **alert** or **infoview** 

Topic for device communication
```sh  
management/<display-id>/update
```  
> Subtopic **"update"** not mandatory and is used only for notifying the aggregator to publish data from a database
## Installation  
  
For running the build on Linux:

Before installing anything make sure operating system is up to date.

Check that your python version is at least 3.9
```sh  
python3 --version
```
Make sure you have git and pip3 installed
```sh  
sudo apt-get update
sudo apt install git 
sudo apt install python3-pip
```  
Clone the repository with git  
```sh  
git clone https://github.com/InnovationProject4/platform-info-system  
```  
Navigate to the "build" folder
  ```sh  
cd platform-info-system/build
```  
Install the requirements.txt file with pip3
```sh  
pip3 install -r requirements.txt  
```  
If your python doesn't come with built-in tkinter package install it
```sh  
sudo apt-get install python3-tk
```  
  
Edit the config.ini file for MQTT brokers IP and port. Also, if your device is running displays you can choose
to have it full screen or windowed.
```sh  
[mqtt-broker]
ip = localhost (Type in the brokers IP)
port = 1883 (Type in the brokers port)

[sqlite]
repository = database.db

[display]
fullscreen = 1 (1 = full screen, 0 = windowed)

[validation]
token = *HIDDEN*
```  
### Management Node

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
  
The aggregator can be executed with the command:  
```sh  
python3 aggregator.py -s <station_short_code(s)> -g <>
```  
> Aggregation of several stations is possible if you separate them with spaces. \
> Adding the -g argument opens up a gui for the aggregator.

The display manager can be executed with the command:  
```sh  
python3 manager_client.py  
```
### Displays  
  
The display can be executed with the command:  
```sh  
python3 display_client.py -view <display_view> -s <station_short_code> -p <platform> -left <platform> -right <platform> -transit<transit> -transport<transport>  
```  
> Here is an explanation of the different parameters:\  
> -view "tableview" requires the parameter -s but -p, -transit and -transport are optional\  
> -view "splitview" requires parameters -s, -left, -right but -transit and -transport are optional\  
> -view "platformview" requires parameters -s and -p but -transit and -transport are optional\  
> -view "infoview" requires only the parameter -s
