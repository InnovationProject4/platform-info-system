import configparser
import json
import sqlite3
import sys
import time

from messaging.telemetry import Connection

db = sqlite3.connect("sqlite3.db")
cursor = db.cursor()
# creates a "topics" table if it does not exist
cursor.execute("CREATE TABLE IF NOT EXISTS topics (id INTEGER PRIMARY KEY, topic TEXT)")

# creates an "announcements" table if it does not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS announcements
                (id INTEGER PRIMARY KEY, topic_id INTEGER, announcement TEXT,
                 FOREIGN KEY (topic_id) REFERENCES topics(id))''')
db.commit()

config = configparser.ConfigParser()
config.read('config.ini')
ip = config.get('mqtt-broker', 'ip')
port = config.get('mqtt-broker', 'port')
# creating a mqtt client
conn = Connection(ip, int(port))

try:
    conn.connect()
except ConnectionRefusedError:
    print("Connection to the broker failed")
    sys.exit()


def publishAnnouncements():
    cursor.execute('SELECT * FROM topics JOIN announcements ON topics.id = announcements.topic_id')
    result_set = cursor.fetchall()

    topics = {}
    # groups the announcements by topic
    for row in result_set:
        topic = row[1]  # topic name from the second column
        announcement = row[4]  # announcement from the fifth column

        # adds the announcements to the list of messages for this topic
        if topic in topics:
            topics[topic].append(announcement)
        else:
            topics[topic] = [announcement]

    for topic, announcements in topics.items():
        print(topic, announcements)
        time.sleep(0.3)
        conn.publish(topic, json.dumps(announcements))
        time.sleep(0.3)


print("Wait for all topics to be published....")
publishAnnouncements()
print("All topics published")

# {"station":"HKI", "trains":[{"track":"1", "scheduledTime":"2023-03-20T15:57:00.000Z"}]}
# mosquitto_pub -t 'station/HKI/1/passing' -m '{"station":"HKI", "trains":[{"track":"1", "scheduledTime":"2023-03-20T17:15:20.000Z"}]}'