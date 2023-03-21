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
    conn = Connection("84.253.229.22", 1883)
    conn.connect()
    conn.set_user_data(json.dumps(message))
    conn.subscribe("station/PSL/1/#", lambda res, user, message:(
        print(message.topic),
        print(message.payload.decode()),
        print()
    ))
    return conn



if __name__ == '__main__':
    conn = initialize()

    try:
        while True:
            time.sleep(10)
    except:
        conn.disconnect()