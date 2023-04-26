from messaging.telemetry import Connection
import time
import json
'''
    connection to rata.digitraffic via tcp/mqtt
'''

message = {
    'test_data': 0
}

def initialize():
    conn = Connection("rata-mqtt.digitraffic.fi", 1883)
    conn.connect()
    conn.set_user_data(json.dumps(message))
    conn.subscribe("trains-by-station/KKN", lambda res, user, message:(
        print(res.json())
    ))
    return conn



if __name__ == '__main__':
    conn = initialize()

    try:
        while True:
            time.sleep(1)
    except:
        conn.disconnect()