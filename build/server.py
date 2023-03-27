from managementNode.manager import Manager
from utils import tkui
# from managementNode.views.brokerstats import MessageStatsView, MessageRateGauge
from managementNode.views.displaystats import DeviceMonitoring, MessageRateGauge

import time, argparse, threading, traceback


parser = argparse.ArgumentParser(description='launch management with dashboard GUI')
parser.add_argument('--gui', action="store_true", help='enter dashboard mode')
parser.add_argument('-g', action="store_true", help='enter dashboard mode')

args = parser.parse_args()


manager = Manager()
DeviceMonitoring.attach(manager.get_displayinfo)

if __name__ == '__main__':
    
    if args.gui or args.g:
        thread = threading.Thread(target=lambda:(
            app := tkui.App(plugins=[
                DeviceMonitoring,
                MessageRateGauge
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
        
       