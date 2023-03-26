import configparser
import json
import sqlite3
import time

config = configparser.ConfigParser()
config.read('config.ini')
repository = config.get('sqlite', 'repository')

db = sqlite3.connect(repository)
cursor = db.cursor()
# creates a "topics" table if it does not exist
cursor.execute("CREATE TABLE IF NOT EXISTS topics (id INTEGER PRIMARY KEY, topic TEXT)")

# creates an "announcements" table if it does not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS announcements
                (id INTEGER PRIMARY KEY, topic_id INTEGER, announcement TEXT,
                 FOREIGN KEY (topic_id) REFERENCES topics(id))''')
db.commit()


def publishAnnouncements(conn):
    print("jotain tapahtuu")
    db2 = sqlite3.connect(repository)
    cursor2 = db2.cursor()
    cursor2.execute('SELECT * FROM topics JOIN announcements ON topics.id = announcements.topic_id')
    result_set = cursor2.fetchall()
    topics = {}
    # groups the announcements by topic
    for row in result_set:
        topic = row[1]  # topic name from the second column
        announcement = row[3]  # announcement from the fifth column

        # adds the announcements to the list of messages for this topic
        if topic in topics:
            topics[topic].append(announcement)
        else:
            topics[topic] = [announcement]

    for topic, announcements in topics.items():
        time.sleep(0.3)
        conn.publish(topic, json.dumps(announcements))
        time.sleep(0.3)
