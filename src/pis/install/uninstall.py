#!/usr/bin/env python3

import os, shutil, subprocess

SERVICE_PATH = '/etc/systemd/system/'

APP_NAME = 'pids'
CONFIG_INI = 'config.ini'
ENC_NAME = 'private.pfx'


if os.path.exists('/usr/local/etc') and os.path.isdir('/usr/local/etc/' + APP_NAME):
    path = f'/usr/local/etc/{APP_NAME}/'
elif os.path.exists('/etc') and os.path.isdir('/etc/' + APP_NAME):
    path = f'/etc/{APP_NAME}/'
elif os.path.exists(f'{os.environ["HOME"]}/.local') and os.path.isdir(f'{os.environ["HOME"]}/.local/share/' + APP_NAME):
    path = f'{os.environ["HOME"]}/.local/share/{APP_NAME}/'  # fallback to /usr/local/etc if neither directory exists
else:
    path = f'/.{APP_NAME}/'  # fallback to /home/.<app_name> if none of the directories are available
    
CONFIG_PATH = path


def del_dir_if_exists(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f'Removed {directory}')
    else:
        print(f'directory {directory} does not exist.')

def systemd_kill_service(service_file, service_name):
    if os.path.exists(SERVICE_PATH + service_file):
        # Stop and disable the systemd service
        subprocess.run(['systemctl', 'stop', service_name])
        subprocess.run(['systemctl', 'disable', service_name])
        os.remove(SERVICE_PATH + service_file)
        print(f'Removed {SERVICE_PATH + service_file} Service')
    else:
        print(f'service file {service_file} does not exist.')
        


del_dir_if_exists(CONFIG_PATH)


files = os.listdir(SERVICE_PATH)
for file in files:
    if file.endswith('.pids.service'):
        systemd_kill_service(file, file)


print('Uninstallation complete.')