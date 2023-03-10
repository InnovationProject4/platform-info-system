import managementNode.manager as manager
import time


if __name__ == '__main__':
    try:
        while True:
            manager.trains.send()
            time.sleep(30)
    except:
        manager.conn.disconnect()

