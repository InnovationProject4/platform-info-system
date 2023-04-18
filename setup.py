#!/usr/bin/env python3

import site, sys, os, shutil, configparser, socket
from setuptools import setup

# workaround bug https://github.com/pypa/pip/issues/7953
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

import build.wizard

APP_NAME = 'pids'
CONFIG_INI = 'config.ini'

if os.name == "posix":
    
    # This code will be executed on Linux
    if os.path.exists('/usr/local/etc'):
        if not os.path.exists('/usr/local/etc'):
            print("Creating directory: /usr/local/etc/" + APP_NAME)
            os.makedirs(f'/usr/local/etc/{APP_NAME}', exist_ok=True)
        path = f'/usr/local/etc/{APP_NAME}/'
    elif os.path.exists('/etc'):
        path = f'/etc/{APP_NAME}/'
    else:
        path = f'/usr/local/etc/{APP_NAME}/'  # fallback to /usr/local/etc if neither directory exists
        print("WARNING: unable to join path, attempting default: " + path)

    INSTALL_DIR = '/opt/pids'
    USR_ETC_DIR = path
    SERVICE_FILE = '/etc/systemd/system/pids.service'

elif os.name == "nt":
    # This code will be executed on Windows
    if not os.path.exists(os.path.join(os.environ['APPDATA'], APP_NAME, CONFIG_INI)):
        #os.mkdir(os.path.join(os.environ['APPDATA'], APP_NAME ))
        print("Creating directory: " + os.path.join(os.environ['APPDATA'], APP_NAME))
        os.makedirs(os.path.join(os.environ['APPDATA'], APP_NAME), exist_ok=True)
        
    path = os.path.join(os.environ['APPDATA'], APP_NAME)
    
    INSTALL_DIR = 'C:\Program Files\pids'
    USR_ETC_DIR = path
    SERVICE_FILE = '%PROGRAMDATA%\pids'
    
    

def prompt(help, **kwargs):
    options = ' '.join(f'[{key}] {val}' for key, val in kwargs.items())
    prompt_args = f'{help} ({"/".join(kwargs)}): '
    prompt_opts = f'Try {options} or [x] to force quit:  '
    kwargs['x'] = "Force quit"
    
    # Prompt the user and get the response
    response = input(prompt_args).lower()
    while response not in kwargs:
        response = input(prompt_opts).lower()

    if response.lower() == 'x':
      print("Aborted by user.")
      exit()
    else:
      return response
  
def find_mqtt_ip():
    ip = ''
    default = '192.168.0.24'
    
    try:
         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         sock.settimeout(0.1)
         sock.connect(("8.8.8.8", 1883))
         ip = sock.getsockname()[0]
         sock.close()
         
    except socket.gaierror:
        print(f"Error: Could not resolve mosquitto ip, using default: {default}")
        return default
    return ip
    
def install():
    # Check if the app is already installed
    print()
    if os.path.exists(INSTALL_DIR):
        print('Warning: passenger-information-system is already installed in {}.'.format(INSTALL_DIR))
        print('Please remove the existing installation before installing a new version.')
        response = prompt('Do you want to remove the existing installation?', y="to remove", n="to abort installation")
        if response.lower() == 'y':
            print('Removing existing installation...')
            shutil.rmtree(INSTALL_DIR)
            shutil.rmtree(USR_ETC_DIR)
            response = prompt('Do you want to continue with the reinstallation?', y="to continue", n="to abort")
            if response.lower() == 'n':
                print('Installation was aborted by user.')
                exit()
                
        else:
            print('Aborting installation.')
            exit()

    # Check if setup.cfg exists
    if not os.path.isfile('setup.cfg'):
        print('setup.cfg not found. Aborting installation.')
        exit()

    setup(use_scm_version=True, data_files=[
            (USR_ETC_DIR, [CONFIG_INI]),
        ])
    
    

    # Create the config.ini file
    config = configparser.ConfigParser()
    config['mqtt-broker'] = {'ip': find_mqtt_ip(), 'port': '1883'}
    config['sqlite'] = {'repository': 'database.db'}
    config['validation'] = {'token': '17adbcf543e851aa9216acc9d7206b96'}
    config['display']  = {"fullscreen" : 1}

    #if os.path.isdir(USR_ETC_DIR) == False:
    try:
        with open(USR_ETC_DIR + 'config.ini', 'w') as f:
            config.write(f)
            print("config.ini created for user")
    except IOError as ex:
        print('Failed to create config.ini', ex)
        

def run_wizard():
    response = prompt("Would you like to run creation wizard now?", y="yes", n="no")
    if response == "y":
        wizard.main()


if __name__ == "__main__":
    install()
    run_wizard()
