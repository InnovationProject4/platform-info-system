from pis.utils.conf import Conf
import json
import sqlite3
import time


repository = Conf().config.get('sqlite', 'repository')

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
    db2 = sqlite3.connect(repository)
    db2.row_factory = sqlite3.Row
    cursor2 = db2.cursor()
    cursor2.execute('SELECT * FROM topics JOIN announcements ON topics.id = announcements.topic_id')
    result_set = cursor2.fetchall()
    topics = {}
    # groups the announcements by topic
    for row in result_set:
        topic = row['topic']
        announcement = row['announcement']

        # adds the announcements to the list of messages for this topic
        if topic in topics:
            topics[topic].append(announcement)
        else:
            topics[topic] = [announcement]

    for topic, announcements in topics.items():
        time.sleep(0.3)
        conn.publish(topic, json.dumps(announcements))
        time.sleep(0.3)
