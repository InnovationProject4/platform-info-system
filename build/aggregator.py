from managementNode.manager import Manager
from utils import tkui
# from managementNode.views.brokerstats import MessageStatsView, MessageRateGauge
from managementNode.views.displaystats import DeviceMonitoring

import time, argparse, threading, traceback


parser = argparse.ArgumentParser(description='launch management with dashboard GUI')
parser.add_argument('-g', '--gui', action="store_true", help='enter dashboard mode')
parser.add_argument('-s', '--station', nargs="+", required=True, help='add which railway station(s) to listen for using shortStationCode')

args = parser.parse_args()


manager = Manager(args.station)
DeviceMonitoring.attach(manager.get_displayinfo)

if __name__ == '__main__':
    
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
            time.sleep(60)
    except:
        traceback.print_exc()
    finally:
        manager.conn.disconnect()
        
       