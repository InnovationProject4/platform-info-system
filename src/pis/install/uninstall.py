#!/usr/bin/env python3

import os, shutil, subprocess

INSTALL_DIR = '/opt/pids'
CONFIG_FILE = '/etc/pids/config.ini'
SERVICE_PATH = '/etc/systemd/system/'

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
        

del_dir_if_exists(INSTALL_DIR)
del_dir_if_exists(CONFIG_FILE)


files = os.listdir(SERVICE_PATH)
for file in files:
    if file.endswith('.pids.service'):
        systemd_kill_service(file, file)


print('Uninstallation complete.')