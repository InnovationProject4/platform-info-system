from managementNode.manager import Manager
import time

manager = Manager()

if __name__ == '__main__':
    try:
        while True:
            print(manager.get_displayinfo())
            manager.trains.send()
            time.sleep(30)
    except Exception as ex:
        manager.conn.disconnect()
        print(ex)

