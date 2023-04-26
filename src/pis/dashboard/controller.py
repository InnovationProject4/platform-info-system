from pis.utils.conf import Conf
import json
import sys
import sqlite3
import tkinter as tk
import uuid

from pis.messaging.telemetry import Connection



repository = Conf().config.get('sqlite', 'repository')
db = sqlite3.connect(repository)
db.row_factory = sqlite3.Row
cursor = db.cursor()

new_uuid = str(uuid.uuid4())

# creates a "topics" table if it does not exist
cursor.execute("CREATE TABLE IF NOT EXISTS topics (id INTEGER PRIMARY KEY, topic TEXT UNIQUE)")

# creates an "announcements" table if it does not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS announcements
                (id INTEGER PRIMARY KEY, announcement TEXT,
                 topic_id INTEGER REFERENCES topics(id))''')
db.commit()

ip = Conf().config.get('mqtt-broker', 'ip')
port = Conf().config.get('mqtt-broker', 'port')
# creating a mqtt client
conn = Connection(ip, int(port))

try:
    conn.connect()
except ConnectionRefusedError:
    print("Connection to the broker failed")
    sys.exit()


def addRow(frame, data, entry):
    if entry.get() == "":  # returns if entry is empty
        return

    # creates a new row of widgets
    row_frame = tk.Frame(frame, bg="#cccccc")
    tk.Grid.columnconfigure(row_frame, 0, weight=1)
    message = tk.Label(row_frame, text=entry.get(), font=('Calibri Light', 9))

    # binds message, so it doesn't go past the frame nor the delete button
    message.bind('<Configure>', lambda e: message.configure(wraplength=(row_frame.winfo_width() - 80)))
    delete_button = tk.Button(row_frame, text='Delete', command=lambda: deleteRow(row_frame, data))

    # packs the widgets into the row frame
    message.grid(row=0, column=0, padx=10, pady=4)
    delete_button.grid(row=0, column=1, sticky="E", padx=(0, 10), pady=4)

    # adds the row to the table
    data.append((message, delete_button))
    row_frame.pack(fill="x", expand=True, pady=2)

    # empties the entry when you add a message
    entry.delete(0, tk.END)


def fillRows(frame, data, items):
    if items is None or len(items) == 0:  # returns if items list from db is empty
        return
    for item in items:
        # creates a new row of widgets
        row_frame = tk.Frame(frame, bg="#cccccc")
        tk.Grid.columnconfigure(row_frame, 0, weight=1)
        message = tk.Label(row_frame, text=item, font=('Calibri Light', 9))

        # binds message so it doesn't go past the frame nor the delete button
        message.bind('<Configure>', lambda e: message.configure(wraplength=(row_frame.winfo_width() - 80)))
        delete_button = tk.Button(row_frame, text='Delete', command=lambda rf=row_frame: deleteRow(rf, data))

        # packs the widgets into the row frame
        message.grid(row=0, column=0, padx=10, pady=4)
        delete_button.grid(row=0, column=1, sticky="E", padx=(0, 10), pady=4)

        # adds the row to the table
        data.append((message, delete_button))
        row_frame.pack(fill="x", expand=True, pady=2)


# removes the row from the table
def deleteRow(row_frame, data):
    for row_data in data:
        if row_data[0].master == row_frame:
            data.remove(row_data)
            break
    # destroys the row's widgets
    row_frame.destroy()


# destroys all elements in a frame
def deleteAllRows(frame):
    for child in frame.winfo_children():
        child.destroy()


def insertToLog(log, msg):
    # log needs to be set to a "normal" state, so it can be edited
    log.configure(state="normal")
    log.insert(tk.END, msg)
    log.see(tk.END)  # keeps the log always moving to the newest message
    log.configure(state="disabled")


def createPopup(title, text):
    popup = tk.Toplevel()
    popup.title(title)
    popup.grab_set()
    label = tk.Label(popup, text=text)
    label.pack(pady=10)
    button = tk.Button(popup, text="Ok", font=('Calibri Light', 10), command=lambda: popup.destroy(), width=10)
    # making sure the popup size is at least more than the label inside it
    popup.geometry(f"{label.winfo_reqwidth() + 100}x{label.winfo_reqheight() + 100}")
    button.pack(pady=10)


def validateEntries(required_entries):
    for entry in required_entries:
        if any(char.isspace() for char in entry.get()) or entry.get() == '':
            return False
    return True


def connectToDisplays(log):
    conn.subscribe_multiple([
        ("management", lambda client, userdata, message: (
            formatDisplayMessage(message.payload.decode(), log)
        ))])


def formatDisplayMessage(msg, log):
    try:
        parsed = json.loads(msg)
        if 'display_name' in parsed['message']:
            insertToLog(log,
                        f"{parsed['event']}: {parsed['message']['uuid']}\n- {parsed['message']['display_name']}\n\n")
        else:
            insertToLog(log, f"{parsed['event']}: {parsed['message']['uuid']}\n\n")
    except Exception:
        print("Key not found in the message")


def connectToAggregator(log):
    conn.subscribe_multiple([
        ("station/#", lambda client, userdata, message: (
            insertToLog(log, f"Publish: {message.topic}\n")
        ))])


# sets a new topic and its corresponding announcements
def dbSet(data, topic):
    # cursor.execute("INSERT OR IGNORE INTO topics (topic) VALUES (?)", (topic,))
    cursor.execute("INSERT INTO topics (topic) SELECT (?) WHERE NOT EXISTS (SELECT 1 FROM topics WHERE topic = ?)",
                   (topic, topic))
    cursor.execute("SELECT id FROM topics WHERE topic = ?", (topic,))
    topic_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM announcements WHERE topic_id = ?", (topic_id,))

    # If the data list is empty, insert an empty announcement for the topic
    if len(data) == 0:
        cursor.execute("INSERT INTO announcements (topic_id, announcement) VALUES (?, ?)",
                       (topic_id, ""))
    else:
        # If the data list is not empty, insert all announcements for the topic
        announcements = [(topic_id, label.cget("text")) for (label, _) in data]
        cursor.executemany("INSERT INTO announcements (topic_id, announcement) VALUES (?, ?)", announcements)

    cursor.execute("SELECT * FROM topics")
    db.commit()
    conn.publish(f"management/{new_uuid}/update", "")
    createPopup("Success", "Success")


# gets the announcements for a specific topic
def dbGet(topic):
    cursor.execute('''SELECT announcements.announcement
                      FROM announcements
                      JOIN topics ON announcements.topic_id = topics.id
                      WHERE topics.topic = ? AND announcements.announcement != "" ''', (topic,))
    announcements = cursor.fetchall()
    announcement_list = [row[0] for row in announcements]
    if announcement_list is None:
        return
    return announcement_list


# clears the tables in the database
def dbClear():
    cursor.execute('DELETE FROM topics')
    cursor.execute('DELETE FROM announcements')
    db.commit()
    createPopup("Success", "Database tables cleared successfully")


# clears the announcements in the database
def dbClearAnnouncements():
    # select distinct topics from the topics table
    cursor.execute("SELECT id FROM topics")
    topics = cursor.fetchall()

    # delete all announcements
    cursor.execute("DELETE FROM announcements")
    print(topics)
    # insert an empty announcement for each topic
    for topic in topics:
        cursor.execute("INSERT INTO announcements (topic_id, announcement) VALUES (?, '')",
                       (topic[0],))
    db.commit()
    conn.publish(f"management/{new_uuid}/update", "")
    createPopup("Success", "Announcements cleared successfully")


# retrieves all data from the topics and announcements tables
def dbGetAll():
    cursor.execute('SELECT * FROM topics JOIN announcements ON topics.id = announcements.topic_id')
    result_set = cursor.fetchall()
    print(result_set)

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

    # make a string of all annonucements and topics and show it in a popup
    string = ""
    for topic, announcements in topics.items():
        string += topic + '\n'
        for announcement in announcements:
            string += '- ' + str(announcement) + '\n'
        string += '\n'
    if string == "":
        text = "No announcements saved"
    else:
        text = string
    createPopup("All announcements", text)


# terminate function for closing db connection
def terminate(root):
    db.close()
    root.quit()
