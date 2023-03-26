from managementNode.manager import Manager
# from utils import tkui
# from managementNode.views.brokerstats import MessageStatsView, MessageRateGauge

import time, argparse, threading, traceback


parser = argparse.ArgumentParser(description='use manager dashboard')
parser.add_argument('--dashboard', type=str, help='enter dashboard mode')
parser.add_argument('-d', type=str, help='enter dashboard mode')

args = parser.parse_args()


manager = Manager()

if __name__ == '__main__':
    
   # if args.dashboard or args.d:
        #thread = threading.Thread(target=lambda:(
        #    app := tkui.App(plugins=[
        #        MessageStatsView,
        #        MessageRateGauge
        #    ]),
        #    
        #    ## Make default viewport
        #    
        #    # Render hierarchy
        #   default_group := tkui.ViewGroup(app.workspace),
        #    default_viewport := tkui.Viewport(default_group),
        #     
        #    # Layout hierarchy
        #    default_group.add_viewport(default_viewport),
        #    app.add_viewgroup(default_group),
        #    
        #    app.run()
        #    
       # )).start()
        
    
    try:
        while True:
            print(manager.get_displayinfo())
            manager.trains.send()
            time.sleep(80)
    except:
        traceback.print_exc()
    finally:
        manager.conn.disconnect()
        
       