from pis.managementNode.manager3 import Manager
from pis.utils import tkui, conf
# from managementNode.views.brokerstats import MessageStatsView, MessageRateGauge
from pis.managementNode.views.displaystats import DeviceMonitoring
import time, argparse, threading, traceback



parser = argparse.ArgumentParser(description='Launch management node in cli or dashboard mode')
parser.add_argument('stations', metavar="StationCode", type=str, nargs="+", help='ShortCodes of railway station(s) to listen for')
parser.add_argument('-g', '--gui', action="store_true", help='Enter dashboard mode')
args = parser.parse_args()

manager = Manager(args.stations)
DeviceMonitoring.attach(manager.get_displayinfo)        

def main():
    print(args.stations)
    
    if args.gui:
        thread = threading.Thread(target=lambda:(
            app := tkui.App(plugins=[
                DeviceMonitoring
            ]),
            
            ## Make default viewport
            
            # Render hierarchy
            default_group := tkui.ViewGroup(app.workspace),
            default_viewport := tkui.Viewport(default_group),
             
            # Layout hierarchy
            default_group.add_viewport(default_viewport),
            app.add_viewgroup(default_group),
            
            app.run()
            
       )).start()

    try:
        while True:
            manager.get_displayinfo()
            manager.trains.send()
            for station in args.stations:
                manager.publish_passing_train_data(station)
            time.sleep(60)
    except:
        traceback.print_exc()
    finally:
        manager.conn.disconnect()
    

if __name__ == '__main__':
    main()
        
