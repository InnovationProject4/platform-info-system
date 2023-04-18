

CONNECTED       = "connected"
DISCONNECTED    = "disconnected"
UNTRUSTED       = "untrusted"

NOCODE          = 0
PLATFORM        = 1
INFO            = 2

class Display:
    '''
    Database Access Object
    
    '''
    def __init__(self, uuid="", pk="", message_timestamp="", start_timestamp="", name="Unknown Device", display_type="", conn=None):
        self.uuid = uuid
        self.pk = pk
        self.display_name = name
        self.display_type = display_type
        self.status = DISCONNECTED
        self.last_message_timestamp = message_timestamp
        self.start_timestamp = start_timestamp
        self.conn = conn


    def schema(self):
        self.conn.cursor().execute('''
        CREATE TABLE IF NOT EXISTS display(
        id INTEGER PRIMARY KEY,
        uuid TEXT unique,
        pk TEXT unique,
        display_name TEXT unique,
        display_type INTEGER,
        status INTEGER,
        last_message_timestamp TIMESTAMP,
        start_timestamp TIMESTAMP
        )''')

        self.conn.commit()
    

    def insert(self, uuid, pk, display_name, display_type, status, message_timestamp, start_timestamp):
        self.conn.execute('''INSERT OR REPLACE INTO display(uuid, pk, display_name, display_type, status, last_message_timestamp, start_timestamp)  \
        VALUES (:uuid, :pk, :display_name, :display_type, :status, :last_message_timestamp, :start_timestamp)''',
        {
            "uuid": uuid,
            "pk": pk,
            "display_name": display_name,
            "display_type": display_type,
            "status": status,
            "last_message_timestamp": message_timestamp,
            "start_timestamp": start_timestamp
        })

        self.conn.commit()


    def fetchall(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT uuid, display_name, display_type, last_message_timestamp, start_timestamp, status FROM display''')
        return cur.fetchall()

    
    def fetchOne(self, uuid=None, display_name=None, status=None):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM display WHERE uuid=? or display_name=? or status=?''', (uuid, display_name, status))
        return cur.fetchOne()


    def update(self, uuid=None, display_name=None, display_type=None, status=None, message_timestamp=None, start_timestamp=None):
        cur = self.conn.cursor()

        columns = {
            'uuid': uuid,
            'display_name': display_name,
            'display_type': display_type,
            'status': status,
            'last_message_timestamp': message_timestamp,
            'start_timestamp': start_timestamp
        }

        set_clauses = []
        for column, value in columns.items():
            if value is not None:
                set_clause = f"{column} = ?"
                set_clauses.append(set_clause)

        set_clause_str = ", ".join(set_clauses)

        query = f"""
            UPDATE display
            SET {set_clause_str}
            WHERE uuid = {uuid} OR display_name = {display_name}
        """

        cur.execute(query, tuple(columns.values()))
        if cur.rows == 0:
            print(f'db: Error updating model: {display_name}')
        else:
            self.conn.commit()
        


    def delete(self, uuid):
        cur = self.conn.cursor()
        cur.execute('''DELETE from display WHERE uuid = ?''', (uuid))
        if cur.rows == 0:
            print(f'db: Error deleting row: {uuid}')
        else:
            self.conn.commit()



    