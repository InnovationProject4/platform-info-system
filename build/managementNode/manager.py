import json
import messaging.ratatraffic as rata
from messaging.telemetry import Connection 


conn = Connection(localhost, 1883)
conn.connect()

#devices on awake attempt to handshake with management
conn.subscribe("management", lambda client, userdata, message : (
    print("device handshake from ", message.topic)
))


STATION = 'PSL'

# select the desired keys from the top-level list
t_filter = ['trainType', 'trainCategory', 'commuterLineID']

# select the desired keys from  the 'timeTableRows' list
tt_filter = ['type', 'cancelled', 'scheduledTime', 'differenceInMinutes', 'liveEstimateTime', 'commercialTrack', 'cause']

def parse(response):
    # TODO: parse response for destination and commuter
    filtered = {key: response[key] for key in t_filter}
    filtered["timeTableRows"] = [{key: row.get(key, None) for key in tt_filter} for row in response['timeTableRows'] if row['stationShortCode'] == STATION]
    return filtered


def publish(trains):
    for train in trains:
        for shift in train['timeTableRows']:
            platform_id = shift.get('commercialTrack', None)
            transit = shift.get('type')
            transport_type = train.get('trainCategory')
        
            topic = f"station/{STATION}/{platform_id}/{transit}/{transport_type}"
            conn.publish(topic, json.dumps(train))

    


trains = rata.Simple('live-trains/station/' + STATION).get(payload={
    'minutes_after_departure': 0,
    'minutes_before_arrival' : 0,
    'minutes_after_arrival': 0,
    'train_categories' : 'Commuter,Long-distance'
}).onSuccess(lambda response, status, data : (
   filtered := [(parse(train)) for train in response.json()],
   publish(filtered)

))