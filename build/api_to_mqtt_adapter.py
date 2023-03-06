import messaging.ratatraffic as rata
from messaging.telemetry import Connection 


# api requests
def adapterSimple():
    # mqtt telemetry connection
    conn = Connection("rata-mqtt.digitraffic.fi", 1883)
    conn.connect()

    rata.Simple('live-trains/station/KKN').get(payload={
        'arrived_trains': 0,
        'arriving_trains': 5,
        'departing_trains': 0,
        'departed_trains': 0,
        'include_nonstopping': 'true'
    }).onSuccess(lambda response, status, data : (
        print("successful fetching"), 
        print(response.json())

        conn.publish("trains/station/KKN", response.json())

    )).onFailure(lambda response, status, data : (
        print(f"Error: {status}") if status == 400 else print(f"Internal Error: {status}"),
        str(data)
    ))


def InformationAdapter():
    # mqtt telemetry connection
    conn = Connection("rata-mqtt.digitraffic.fi", 1883)
    conn.connect()

    



