#!/usr/bin/env python3
import os, shutil, configparser, socket
# Post install configutation. Can be used to refresh configs on errors.

APP_NAME = 'pids'
CONFIG_INI = 'config.ini'
ENC_NAME = 'private.pfx'

if os.name == "posix":
    
    # This code will be executed on Linux
    if os.path.exists('/usr/local/etc') and os.access('/usr/local/etc', os.W_OK):
        if not os.path.exists('/usr/local/etc/' + APP_NAME) and not os.path.isdir('/usr/local/etc/' + APP_NAME):
            print("Creating directory: /usr/local/etc/" + APP_NAME)
            os.makedirs(f'/usr/local/etc/{APP_NAME}', exist_ok=True)
        path = f'/usr/local/etc/{APP_NAME}/'
        
    elif os.path.exists('/etc') and os.access('/etc', os.W_OK):
        if os.path.isdir('/etc/' + APP_NAME):
            print("Creating directory: /etc/" + APP_NAME)
            os.makedirs(f'/etc/{APP_NAME}', exist_ok=True)
        path = f'/etc/{APP_NAME}/'
        
    elif os.path.exists(f'{os.environ["HOME"]}/.local') and os.access(f'{os.environ["HOME"]}/.local', os.W_OK):
        path = f'{os.environ["HOME"]}/.local/share/{APP_NAME}/'  # fallback to /home/.local/share if neither directory exists
        print("Warning: Unable to join user path, attempting default path: " + path)
        if not os.path.isdir(f'{os.environ["HOME"]}/.local/share/{APP_NAME}/'):
            os.makedirs(f'{os.environ["HOME"]}/.local/share/{APP_NAME}/', exist_ok=True)
            print(f'Creating directory: {os.environ["HOME"]}/.local/share/' + APP_NAME)
            
    else:
        path = f'/.{APP_NAME}/'  # fallback to the old ways of /home/.<app_name> if none of the directories are available
        print("Warning: Unable to join path, attempting fallback path: " + path)
        os.makedirs(f'/.{APP_NAME}/', exist_ok=True)
        print("Creating directory: /." + APP_NAME)
        

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
    # Attempt to locate the ip of the mosquitto broker, otherwise use default ip and customize later
    ip = ''
    default = 'localhost'
    
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


def create_config():
    # Create the config.ini file
    config = configparser.ConfigParser()
    config['mqtt-broker'] = {'ip': find_mqtt_ip(), 'port': '1883'}
    config['sqlite'] = {'repository': 'database.db'}
    config['display']  = {"fullscreen" : 1}
    config['validation'] = {'token': ''}
    
    try:
        with open(USR_ETC_DIR + CONFIG_INI, 'w') as f:
            config.write(f)
            print("config created in " + USR_ETC_DIR + "")
    except IOError as ex:
        print('Failed to create config', ex)

        
        
    
def install():
    if os.path.isfile(USR_ETC_DIR + CONFIG_INI):
        print("Warning: config already exists in " + USR_ETC_DIR + ".")
        response = prompt("Overwrite config?", y="Overwrite the config file", n="Keep the existing config file")
        if response == "y":
            create_config()
        else: 
            print("Keeping existing config")
    else:
        create_config()
        
    if not os.path.isfile(USR_ETC_DIR + ENC_NAME):
        import pis.utils.conf as conf
        
        conf.CONFIG_PATH = os.path.join(path, CONFIG_INI)
        conf.ENC_PATH = os.path.join(path, ENC_NAME)
        
        from pis.install.wizard import prompt_confirmpassword, generate_validation_keys
        import pis.utils.integrity as integrity
        
        print("No validation token found. Generating new one...")
        print("Validation uses encrypted storage. Please enter a password to encrypt the token.")
        pfk = prompt_confirmpassword()
        generate_validation_keys(pfk, None, integrity)
        

if __name__ == "__main__":
    install()