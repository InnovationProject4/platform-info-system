import os, sys, configparser
from utils.Singleton import _Singleton

'''
Global configurations. The location of the config file depends on the underlying OS. in module should run once.

On windows the config file is located in the User's %AppData% folder.
On Linux the config file is located in the /etc folder.

'''

APP_NAME = 'pids'
CONFIG_INI = 'config.ini'
ENC_NAME = 'private.pfx'

if os.name == "posix":
    # This code will be executed on Linux
    if os.path.exists('/usr/local/etc'):
        path = f'/usr/local/etc/{APP_NAME}/'
    elif os.path.exists('/etc'):
        path = f'/etc/{APP_NAME}/'
    else:
        path = f'/usr/local/etc/{APP_NAME}/'  # fallback to /usr/local/etc if neither directory exists
        print("unable to join path, attempting default: " + path)
    

    
    
elif os.name == "nt":
    # This code will be executed on Windows
    if not os.path.exists(os.path.join(os.environ['APPDATA'], APP_NAME, CONFIG_INI)):
        print("Path does not exist: " + os.path.join(os.environ['APPDATA'], APP_NAME))
      
        
    path = os.path.join(os.environ['APPDATA'], APP_NAME)
    
script_dir = os.path.dirname(os.path.abspath(__file__))

WORKING_DIR = os.path.dirname(script_dir)
CONFIG_PATH = os.path.join(path, CONFIG_INI)
ENC_PATH = os.path.join(path, ENC_NAME)

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

global ADDR, PORT, TOKEN
ADDR = config.get('mqtt-broker', 'ip')
PORT = config.getint('mqtt-broker', 'port')

if config.has_section('validation') and config.has_option('validation', 'token'):
    TOKEN = config.get('validation', 'token')


class Conf(_Singleton):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_PATH)
        self.config_path = path
        self.work_path = WORKING_DIR
        self.enc_path = ENC_PATH
        
    @property
    def get(self, section, key):
        return self.config(section, key)