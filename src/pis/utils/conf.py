import os, sys, configparser
from pis.utils.Singleton import _Singleton

'''
Global configurations. The location of the config file depends on the underlying OS. in module should run once.

On windows the config file is located in the User's %AppData% folder.
On Linux the config file is located in the /etc folder, but defaults to users home directory.

'''

APP_NAME = 'pids'
CONFIG_INI = 'config.ini'
ENC_NAME = 'private.pfx'

if os.name == "posix":
    
    # This code will be executed on Linux
    if os.path.exists('/usr/local/etc') and os.path.isdir('/usr/local/etc/' + APP_NAME):
        path = f'/usr/local/etc/{APP_NAME}/'
    elif os.path.exists('/etc') and os.path.isdir('/etc/' + APP_NAME):
        path = f'/etc/{APP_NAME}/'
    elif os.path.exists(f'{os.environ["HOME"]}/.local') and os.path.isdir(f'{os.environ["HOME"]}/.local/share/' + APP_NAME):
        path = f'{os.environ["HOME"]}/.local/share/{APP_NAME}/'  # fallback to /usr/local/etc if neither directory exists
    else:
        path = f'/.{APP_NAME}/'  # fallback to /home/.<app_name> if none of the directories are available

    USR_ETC_DIR = path
    SERVICE_FILE = '/etc/systemd/system/pids.service'

elif os.name == "nt":
    # This code will be executed on Windows
    path = os.path.join(os.environ['APPDATA'], APP_NAME)
    
    INSTALL_DIR = 'C:\Program Files\pids'
    USR_ETC_DIR = path
    SERVICE_FILE = '%PROGRAMDATA%\pids'
    
    
    
script_dir = os.path.dirname(os.path.abspath(__file__))

WORKING_DIR = os.path.dirname(script_dir)
CONFIG_PATH = os.path.join(path, CONFIG_INI)
ENC_PATH = os.path.join(path, ENC_NAME)

global ADDR, PORT, TOKEN

class Conf(_Singleton):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = path
        self.work_path = WORKING_DIR
        self.enc_path = ENC_PATH
        
        if(len(self.config.read(CONFIG_PATH)) == 0):
            print("No config file found. Please run 'pis init' to configure options and validation keys.")
            raise SystemExit
        
        global ADDR, PORT, TOKEN
        ADDR = self.config.get('mqtt-broker', 'ip')
        PORT = self.config.getint('mqtt-broker', 'port')
        TOKEN = self.config.get('validation', 'token')
        
    @property
    def get(self, section, key):
        return self.config(section, key)