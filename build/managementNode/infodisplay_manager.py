import threading
import time
import uuid
from collections import deque
import paho.mqtt.client as paho

client = paho.Client()

# Create a dictionary of queues to store messages for each station
queues = {}


# publishes messages from the queues to the appropriate MQTT topics
def publish_messages():
    while True:
        for station_code, queue in queues.items():
            if len(queue) == 0:
                continue
            message = queue[0]
            # Extract the station code from the message payload
            parts = message.split(" ")
            if len(parts) < 2:
                print("Invalid message:", message, "Example of correct format:HKI message")
                continue
            station_short_code = parts[0]
            message_text = " ".join(parts[1:])

            # Publish only the message text to the appropriate topic
            topic = f"station/{station_code}/informationDisplay"
            client.publish(topic, message_text)

            # Rotate the queue
            queue.rotate(-1)
        time.sleep(5)


# Create a new thread to run the publish_messages function
timer_thread = threading.Thread(target=publish_messages)
timer_thread.start()


# subscribes to the topics we are sending information to
def on_connect(client, userdata, flags, rc):
    print("connected")
    client.subscribe("station/information")
    client.subscribe("station/remove")


# function is called when a message is received on any of the subscribed topics
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    if message.topic == "station/information":
        # Extract the station code from the message payload
        parts = payload.split(" ")
        if len(parts) < 2:
            print("Invalid message:", payload, "Example of correct format: HKI message")
            return
        station_code = parts[0]
        message_uuid = str(uuid.uuid4())

        # Add the message with UUID to the appropriate queue
        message_with_uuid = f"{message_uuid} {' '.join(parts[1:])}"  # remove the station code from the message
        if station_code not in queues:
            queues[station_code] = deque()
        queues[station_code].append(message_with_uuid)
        print(f"Added message {message_uuid} to {station_code} queue: {message_with_uuid}")

    elif message.topic == "station/remove":
        # Remove the message with the given UUID from all queues
        uuid_to_remove = payload.strip()
        print(f"Received message on topic station/remove: {uuid_to_remove}")
        for station_code, queue in queues.items():
            for message in queue:
                if uuid_to_remove == message.split(" ")[0]:
                    queue.remove(message)
                    print(f"Removed message with UUID {uuid_to_remove} from {station_code} queue")
                    break  # exit the inner loop after removing the message


# Set the on_connect and on_message callback functions for the MQTT client
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker and start the event loop
client.connect("localhost", 1883, 60)
client.loop_forever()
