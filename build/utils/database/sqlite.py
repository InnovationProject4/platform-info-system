import sqlite3
from utils.Singleton import Singleton


# TODO: use this on dao.insert
def safeExecute(conn, transaction, values):
    cur = conn.cursor()
    try:
        cur.execute(transaction, values)
        conn.commit()
    except sqlite3.IntegrityError:
        print("db: Dublicate already exists")
        conn.rollback()


class Connection:
    '''
    with SQLiteConnectionManager('example.db') as (conn, cur):
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 25))
        cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 30))
        cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Charlie', 35))
        conn.commit()

    with SQLiteConnectionManager('example.db') as (conn, cur):
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    '''
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cur = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cur = self.conn.cursor()
            self.cur.execute('PRAGMA foreign_keys = ON')
            self.conn.commit()
            print(f'db: Connected: {self.db_file}')
            return self.conn, self.cur
        
        except sqlite3.IntegrityError:
            print("Duplicate already exists")

        except sqlite3.Error as ex:
            self.conn.rollback()
            raise ex
        
        except Exception as ex:
            self.conn.rollback()
            raise ex

        finally:
            if self.conn:
                self.conn.close()

    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cur: self.cur.close()
        if self.conn: 
            self.conn.close()
            print("db: Disconnected")

        if exc_type:
            print(f'Exception Type: {exc_type} occurred. Rolling back transcation changes')
            print(f'Exception Value: {exc_val}')
            print(f'Exception Traceback: {exc_tb}')
            self.conn.rollback()
            return True



class PersistentConnection(Singleton):
    ''' 
    Persistent connection for in-memory databases. Note: that *all* data is lost when connection closes.
    On error, the connection will attempt to backup db to user defined file. On default backup is saved in '.db_backup'
    '''
    def __init__(self, archive_db=".db_backup", nobackup=True): # TODO Make single threaded, currently connection in Singleton
        #self._connection = None
        self.archive_db = archive_db
        self.nobackup = nobackup

    def __enter__(self):
        if not self._connection:
            self._connection = sqlite3.connect(":memory:")
            self._connection.cursor().execute('PRAGMA foreign_keys = ON')
            self._connection.commit()
            print(f'db: connected in-memory')

        return self._connection, self._connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.nobackup: self.archive_db()
        #self._connection.close()
        if exc_type:
            print(f'Exception Type: {exc_type} occurred. Connection closed (backup initiated)')
            print(f'Exception Value: {exc_val}')
            print(f'Exception Traceback: {exc_tb}')
            #return True
        

    def backup(self):
        '''Backup the current in-house database'''
        try:
            archive = sqlite3.connect(self.archive_db)
            with self._connection as conn:
                conn.backup(archive)

        except Exception as ex:
            print("db: failed to archive in-memory data")
            raise ex

        finally:
            archive.close()

        
    def close(self):
        if self._connection: self._connection.close()
        self.conn = None
        print("db: Persistent connection has closed (user call)")






def simple_execute(file, transaction, values):
    try:
        conn = sqlite3.connect(file)
        cur = conn.cursor()
        #self.cur.execute('PRAGMA foreign_keys = ON')
        #self.conn.commit()
        print(f'db: Connected: {file}')
        cur.execute(transaction, values)
        return conn, cur
    
    except sqlite3.IntegrityError:
        print("Duplicate already exists")

    except sqlite3.Error as ex:
        conn.rollback()
        raise ex
    
    except Exception as ex:
        conn.rollback()
        raise ex

    finally:
        if conn: conn.close()