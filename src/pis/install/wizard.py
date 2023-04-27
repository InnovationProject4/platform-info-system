#!/usr/bin/env python3

import os, sys, shutil, subprocess, re, hashlib, argparse
from pis.install import stationCodes
from tabulate import tabulate
import pis.utils.conf as conf

'''
Management wizard for passenger information system.
Directs the user to easily manage configurations and initialize services.
'''
parser = argparse.ArgumentParser(description='Quick setup')
parser.add_argument('init', nargs='?', default=False, help='Initialize configuration data')
args = parser.parse_args()

if os.name == "posix":
    # This code will be executed on Linux
    import termios, tty
    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)  # or tty.setraw(fd) for raw mode.
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, old)
    
    def check_services():
        return subprocess.check_output(['systemctl', 'list-units', '--type=service', '--state=active', '--no-legend', '--no-pager', '--all', '*.pids.service*'], encoding='utf-8')
    
    def grep(sstring, file):
        try:
            result = subprocess.run(['grep', sstring, file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            
            if result.returncode == 0:
                return result.stdout.strip().split("\n")
            else:
                print("no matching keys found.")
        
        except subprocess.CalledProcessError as e:
            print(e.output)
            print(e.stderr)
        
    def clear(after=None):
        os.system("clear")
        if after is not None:
            after()
            
    HANDLE  = '\x1b'        
    UP      = 'A'
    DOWN    = 'B'
    LEFT    = 'K'
    RIGHT   = 'M'
    ENTER   = '\n'
    SPACE   = ' '
    BACKSPACE = "\x7f"
    
    
    def prompt_password(prompt='Password: ', stream=None):
        """Prompt for password with echo off, using Unix getch()."""
        for c in prompt:
            sys.stdout.write(c)
            sys.stdout.flush()
        pw = ""
        while True:
            c = getch()
            if c == ENTER or c == ' ':
                print()
                return pw
            elif c == BACKSPACE:
                if len(pw) == 0:
                    continue
                pw = pw[:-1]
                print('\b \b', end='', flush=True)
            else:    
                pw += c
                print('*', end='', flush=True)
            
    
    
elif os.name == "nt":
    # This code will be executed on Windows
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
    
    def check_services():
        return subprocess.check_output(['sc', 'query', 'type=', 'service', 'state=', 'running', '|', 'findstr', 'pids'], shell=True, encoding='utf-8')
    
    def clear(after=None):
        os.system("cls")
        if after is not None:
            after()
            
    def grep(sstring, file):
        try:
            result = subprocess.run(['findstr',  sstring, file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                return result.stdout.strip().split("\r\n")
            else:
                print("no matching keys found.")
        
        except subprocess.CalledProcessError as e:
            print(e.output)
            print(e.stderr)
            
    HANDLE  = '\x00'        
    UP      = 'H'
    DOWN    = 'P'
    LEFT    = 'K'
    RIGHT   = 'M'
    ENTER   = '\r'
    SPACE   = ' '
    BACKSPACE = '\b'
    
    def prompt_password(prompt='Password: ', stream=None):
        """Prompt for password with echo off, using Windows getch()."""
        for c in prompt:
            msvcrt.putch(c.encode())
        pw = ""
        while True:
            c = msvcrt.getch().decode()
            if c == ENTER or c == '  ':
                msvcrt.putch('\r'.encode())
                msvcrt.putch(' '.encode())  # extra space after the password
                return pw
            elif c == BACKSPACE:
                if len(pw) == 0:
                    continue
                pw = pw[:-1]
                msvcrt.putch('\b'.encode())
                msvcrt.putch(' '.encode())
                msvcrt.putch('\b'.encode())
            else:
                pw += c
                msvcrt.putch('*'.encode())

def prompt_confirmpassword():
    pwd = hashlib.sha256(prompt_password("Enter new password: ").encode()).digest()
    while True:
        confrm = hashlib.sha256(prompt_password("Confirm new password: ").encode()).digest()
        if pwd == confrm:
            return pwd


def color(text, color, optional=None):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "light_gray": "\033[37m",
        "dark_gray": "\033[90m",
        "light_red": "\033[38;5;9m",
        "light_blue": "\033[38;5;75m",
        "light_cyan": "\033[38;5;14m",
        "end": "\033[0m"
    }
    if text is None: 
        if optional is None: optional = color
        return colors[optional] + "None" + colors["end"]
    else: return colors[color] + text + colors['end']
        
def fuzzy_search(query, texts):
    """Filter a list of texts to only include those that match a fuzzy search."""
    pattern = f'.*{query}.*'  # Build regex pattern to match query
    regex = re.compile(pattern, re.IGNORECASE)  # Compile regex
    return [text for text in texts if regex.search(text)]

def prompt(prompt, commands):
    response = input(prompt).lower()
    while response not in commands:
        print(f"Invalid command: {response}", flush=True)
        response = input(prompt).strip()
    return response
    
def prompt_option(help, **kwargs):
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
        
def prompt_radioGroup(help, options, after=None):
    selected = 0
    selection_max = len(options)
    
    while True:
        clear(after)
        print(help)
        for i, option in enumerate(options):
            if i == selected:
                print("[*] " + option)
            else:
                print("[ ] " + option)
                
        print("Selected:", options[selected])
        key = getch()
        
        if key == UP or key == "A":  # Up arrow
            selected = (selected - 1) % selection_max
        elif key == DOWN or key == "B":  # Down arrow
            selected = (selected + 1) % selection_max
            
        # Exit on enter
        elif key == ENTER:
            return options[selected]

def prompt_checklist(help, checklist, offset=10, limit=10, queryString="", after=None):
    '''multi-selection checklist that works with large lists with optional fuzzy string filter'''
    
    # Define the initial cursor position and scroll offset
    cursor_pos = 0
    scroll_offset = 0
    selected=[]
    
    options = checklist

    while True:
        clear(after)
        print(help)
        # Determine the subset of options to display in the grid
        visible_options = options[scroll_offset:scroll_offset + offset]

        # Display the options
        for i, option in enumerate(visible_options):
            abs_index = scroll_offset + i
            if abs_index == cursor_pos:
                prefix = "> "
            else:
                prefix = "  "
            if option in selected:
                prefix += "[x] "
            else:
                prefix += "[ ] "
            print(prefix + option)
            
        if queryString != "": print("filter for: " + queryString)

        # Prompt the user for input
        ch = getch()
        if ch == SPACE:
            if options:
                if options[cursor_pos] in selected:
                    selected.remove(options[cursor_pos])
                else:
                    if len(selected) < limit:
                        selected.append(options[cursor_pos])
        elif ch == "\r":
            if selected:
                return selected
        elif ch == ENTER:
            if selected:
                return selected
        elif ch == HANDLE:
            if os.name == 'posix': getch() # Consume the second byte of an arrow key sequence
            ch = getch()
            if ch == UP or ch == LEFT:
                cursor_pos = max(0, cursor_pos - 1)
                if cursor_pos < scroll_offset:
                    scroll_offset = cursor_pos
            elif ch == DOWN or ch == RIGHT:
                cursor_pos = min(len(options) - 1, cursor_pos + 1)
                if cursor_pos >= scroll_offset + offset:
                    scroll_offset = cursor_pos - (offset - 1)
                    
        elif ch == BACKSPACE:
            queryString = queryString[:-1] # Remove latest letter on backspace
            options = fuzzy_search(queryString, checklist)
        else:
            print(ch)
            queryString += str(ch)
            options = fuzzy_search(queryString, checklist)
        print(ch)
        
def generate_validation_keys(pfk, config, integrity, after=None):
    def visualize_hashkey(pk):
        color_map = {
            0:  ['/', '\033[48;5;16m'],   # black
            1:  ['-', '\033[48;5;1m'],    # red
            2:  ['\\', '\033[48;5;2m'],    # green
            3:  ['|', '\033[48;5;3m'],    # yellow
            4:  ['_', '\033[48;5;4m'],    # blue
            5:  [' ', '\033[48;5;5m'],    # magenta
            6:  ['+', '\033[48;5;6m'],    # cyan
            7:  ['-', '\033[48;5;7m'],    # white
            8:  ['=', '\033[48;5;8m'],    # bright black
            9:  ['B', '\033[48;5;9m'],    # bright red
            10: ['C', '\033[48;5;10m'],  # bright green
            11: ['E', '\033[48;5;11m'],  # bright yellow
            12: ['F', '\033[48;5;12m'],  # bright blue
            13: ['H', '\033[48;5;13m'],  # bright magenta
            14: ['I', '\033[48;5;14m'],  # bright cyan
            15: ['G', '\033[48;5;15m'],  # bright white
        }

        # Print the key data as a hex grid
        line_len = 64
        for i, byte in enumerate(pk):
            if i % line_len == 0:
                print()
            c = color_map[byte >> 4][1] + color_map[byte & 0x0F][1]  # use the first and second nibble as the color code
            print(f'{c}{color_map[byte >> 4][0]}\033[0m', end='')
        print('\033[0m', flush=True)  # reset the color to default at the end
        print()
        
        
    cert, pfx = integrity.keygen()
    prk = hex(pfx.to_cryptography_key().private_numbers().d)[2:].encode()
    pvk = hex(cert.get_pubkey().to_cryptography_key().public_numbers().n)[2:].encode()

    print("Private Key")
    visualize_hashkey(prk)
    
    print("Public Key")
    visualize_hashkey(pvk)
    
    response = prompt_option(color("Use generated keys?", "yellow"), y="yes", n="no")
    if response == "y":
        
        if config is not None:
            if not config.has_section("validation"):
                config.add_section("validation")
            
            config.set("validation", "token", pfk.hex())
        
        
        integrity.dump(pfx, cert, pfk.hex(), conf.ENC_PATH, conf.CONFIG_PATH)
        
        clear(after=after)
        print(color("Keys were successfully generated and added!", "green"))
    
        
def print_list_services():
    '''get a list of information system services that are active'''
    try:
        services = check_services()
        
        table = []
        for line in services.split('\n'):
            if line:
                name, status, description = line.split(maxsplit=2)
                table.append([name, status, description])
        
        if table: 
            # Print the table
            print("currently active services: ")
            print('{:<50}{:<10}{}'.format('Name', 'Status', 'Description'))
            print('-' * 70)
            for row in table:
                print('{:<50}{:<10}{}'.format(*row))
            print('-' * 70)
        
    except subprocess.CalledProcessError as e:
        print(f"Command returned non-zero exit status {e.returncode}: {e.output}")
        
        
        
def create_service_file(service_name, description="platform-info-system service", pyfile="default.py", argsline=""):
    
    service_path = f"/etc/systemd/system/{service_name}.service"

    
    with open(service_path, "w") as f:
        f.write(f"""
        [Unit]
        Description={description}
        After=network.target
        
        [Service]
        Type=simple
        KillSignal=SIGINT
        Environment=DISPLAY=:0
        WorkingDirectory={os.path.dirname(os.getcwd())}
        ExecStart=/usr/bin/python3 {os.path.join(os.path.dirname(os.getcwd()), pyfile)} { argsline }
        Restart=always

        [Install]
        WantedBy=multi-user.target
        """)
        
    return service_path
    
def install_service(service_path):
    if not os.path.isfile(service_path):
        shutil.copy(service_path, "/etc/systemd/system/")
        
    os.system("systemctl daemon-reload")
    os.system(f"systemctl enable {service_path}")
    os.system(f"systemctl start {os.path.splitext(os.path.basename(service_path))[0]}")
  
    
      
def run_display_wizard():
    '''build a display service'''
    view = None
    station = None
    platform = None
    left = None
    right = None
    transit = None
    transport = None
                
        
    def build_args_string():
        ret = ""
        args = [('-view', view), ('-s', station), ('-transit', transit), ('-transport', transport)]
        for arg, value in args:
            if value is not None:
                ret += f'{arg} {value} '
                
                if arg == "-view" and value == "splitview":
                    ret += f'-left {left} -right {right} '
                elif arg == "-view":
                     ret += f'-p {platform} '
        return ret
    
    def banner():
        print("Display Creation Wizard!")
        print(tabulate([
            ["-view", "viewtype: tableview, platformview, splitview, infoview"],
            ["-s", "Railway station shortCode ex. HKI (Helsinki Asema)"],
            ['-p', 'Platform number ex. 1'],
            ['-left', "Platform number for the left pane in splitview"],
            ['-right', "Platform number for the right pane in splitview"],
            ['-transit', "Type of transit: departures, arrivals (OPTIONAL)"],
            ['-transport', "Type of transport: commuter, long_distance (OPTIONAL)"],
        ]))
        print()
        print(f' {color("-view", "light_blue")} {color(view, "green", "red")} {color("-s", "light_blue")} {color(station, "green", "red")} {color("-p", "light_blue")} {color(platform, "green", "red")} {color("-left", "light_blue")} {color(left, "green", "red")} {color("-right", "light_blue")} {color(right, "green", "red")} {color("-transit", "light_blue")} {color(transit, "green", "red")} {color("-transport", "light_blue")} {color(transport, "green", "red")} ')
        print()
        
         
    view = prompt_radioGroup("Select display viewtype: ", ['tableview', 'platformview', 'splitview', 'infoview'], after=banner)
    if view == "splitview":
        left = input("Type left platform: ")
        right = input("Type right platform: ")
    else:
        clear(after=banner)
        platform= input("Type platform: ")
        if platform == "":
            platform = None
        
    station = (prompt_checklist("Select railway station(s) you want to listen for. Press SPACE to select: ", [' '.join(t) for t in stationCodes.names], after=banner, limit=1))[0].split(" ")[0]
    
    transit = prompt_radioGroup("Select transit type: ", ['departures', 'arrivals', "None"], after=banner)
    transport = prompt_radioGroup("Select transport type: ", ['commuter', 'long_distance', "None"], after=banner)
    
    clear(after=banner)
    
    choices = ['Run with python', 'Run in background', "Install systemd service (Experimental)"]
    
    response = prompt_radioGroup("How do you want to run the Display? Press ENTER to select: ", choices, after=banner)
    if response == choices[0]:
        clear(after=banner)
        
        response = prompt_option(color("Run display with python now?", "yellow"), y="yes", n="no")
        if response == "y":
            commands = ["pis-display"] + build_args_string().strip().split(" ")
            res = subprocess.run(commands, stdout=subprocess.PIPE)
            print(res.stdout.decode('utf-8'))
    
        
    elif response == choices[1]:
        clear(after=banner)
        pass
    
    
    
    elif response == choices[2]:
        print(color("This feature is experimental and may not work on your system. Proceed with caution!", "red"))
        response = prompt_option("Create display service file?", y="yes", n="no")
        if response == "y":
            service_file = create_service_file(f'{view}_{station}.pids', f'Display service for {view} at {station} platform {platform}', "display_client.py", build_args_string())
            
            response = prompt_option("Install display service?", y="yes", n="no")
            if response == "y":
                install_service(service_file)
    
    
    response = prompt_option("continue?", y="yes", n="no")
   
 
def run_aggregator_wizard():
    stations = []
    gui = ""
    
    def build_args_string(append=""):
        if not stations:
            append = "None"
        else:
            for each in stations:
                append += f'{each} '
        return append
            
    
    def banner():
        print("Aggregator Creation Wizard!")
        print(tabulate([
            ["-s, -station", "one or multiple station shortCodes: ex. HSL (Helsinki Asema)"],
            ["-g, -gui", "execute with the UI editor on the side"]
        ]))
        col = "red" if len(stations) == 0 else "green"
        print(f'{color(gui, "light_blue")} {color("-s", "light_blue")} {color(build_args_string(), col)}')
        
        
    selected = (prompt_checklist("Select railway station(s) you want to listen for. Press SPACE to select: ", [' '.join(t) for t in stationCodes.names], after=banner))
    for station in selected:
        stations.append(station.split(" ")[0])
    
    
    clear(after=banner)
    response = prompt_option("launch with graphical user interface?", y="yes", n="no")
    if response == "y":
        gui = "--gui"
        
    clear(after=banner)
    
    choices = ['Run with python', 'Run in background', "Install systemd service (Experimental)"]
    
    response = prompt_radioGroup("How do you want to run Aggregation? Press ENTER to select: ", choices, after=banner)
    
    
    if response == choices[0]:
        clear(after=banner)
        response = prompt_option(color("Run aggregator with python now?", "yellow"), y="yes", n="no")
        if response == "y":
            commands = ["pis-aggregator", ] + stations
            proc = subprocess.run(commands, encoding='UTF-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            
    elif response == choices[1]:
        if gui != "":
            print(color("WARNING: GUI is not supported in background mode.", "red"))
            print("<continue>")
            response = getch()
            return
        
        commands = ["pis-aggregator", ] + stations
        p = subprocess.Popen(commands, stdout=subprocess.PIPE)
        p.communicate()
        
        clear(after=banner)
    
    
    
    elif response == choices[2]:
        print(color("This feature is experimental and may not work on your system. Proceed with caution!", "red"))
        response = prompt_option("Create display service file?", y="yes", n="no")
        if response == "y":
            service_file = create_service_file(f'aggregator.pids', f'Data aggregator for platform-info-system', "aggregator.py", build_args_string(gui + " -s "))
            
            response = prompt_option("Install aggregation service?", y="yes", n="no")
            if response == "y":
                install_service(service_file)
    
    
    response = prompt_option("continue?", y="yes", n="no")
    
    
    

def run_config_wizard():
    dirty=False
    
    config = conf.Conf().config
    
    def banner():
        print("Configuration Wizard!", end="\n")
        print()
        print(tabulate([
            ['Command', 'Description'],
            ["edit", "edit a stored value in sections"],
            ["add <section> <key> <value>", "add a new key-value pair to section"],
            ["rm <section> <key>", "remove a key-value pair from section"],  
            ["grep <some key|some value>", "search for a key-value pair"],
            ["gen", "Generate encrypted validation key for data signing"],
            ["ls", "list all sections"],
            ["save", "commit and save all changes"],
            ["exit", "save modified config and exit the wizard"],
            ["help", "show this banner"],
            [color("config location", "purple"), color(f"{ conf.CONFIG_PATH }", "purple")],
        ], headers="firstrow"))
        if dirty:
            print(color("There are unsaved changes in config awaiting for user action.", "blue"))
        print()
        
    
    clear(after=banner)
    while True:

        command = input(f'wizard# ({color("*config", "yellow") if dirty else color("config", "green")}):  ')
        
        if command == "exit":
            if dirty:
                response = prompt_option(color("Config buffer was modified. Save changes?", "yellow"), y="yes", n="no")
                if response == "y":
                    try:
                        with open(conf.CONFIG_PATH, "w") as f:
                            config.write(f)
                        dirty=False
                        clear(after=banner)
                        print(color("Changes were saved!", "green"))
                    except:
                        print("Could not save changes!")
            break
                
        elif command == "save":
            response = prompt_option(color("Save changes?", "yellow"), y="yes", n="no")
            if response =="y":
                try:
                    with open(conf.CONFIG_PATH, "w") as f:
                        config.write(f)
                    dirty=False
                    clear(after=banner)
                    print(color("Changes were saved!", "green"))
                        
                except Exception as e:
                    print(color("Warning: Could not save changes!", "red"))
                    print(e)
                    
            else: 
                clear(after=banner)
                print("No changes were saved.")
                    
        elif command.startswith("grep"):
            key = command.split(" ")[1:]
            if len(key) == 0:
                print(color("Error: No key or value was given!", "red"))
                continue
            
            group = grep(str(key[0]), conf.CONFIG_PATH)
            if group:
                print()
                for i in group:
                    print(i)
                    
                print()
                print("Found", len(group), "matches.")         
            
        elif command.startswith("edit"):
            try:
                section = prompt_radioGroup("Select section to edit. Press ENTER to continue: ", config.sections())
                key = prompt_radioGroup("Select key to edit. Press ENTER to continue: ", [k for k, v in config[section].items()])
                
                print("editing key", key, "in section", section)
                print("current value:", config[section][key])
                
                value = input(color("new value: ", "yellow"))
                

                response = prompt_option(color("continue? [x] to abort.", "yellow"), y="yes", n="no")
                if response == "y":
                    config.set(section, key, value)
                    dirty = True
                    
                    clear(after=banner)
                    print(color("Value was successfully changed!", "green"))
            
            except Exception as e: 
                print(e)
                print(color("Error: Invalid command!", "red"), str(command))
            
        elif command.startswith("add"):
            try:
                keys = command.split(" ")[1:]
                
                if len(keys) == 1:
                    section = keys[0]
                    
                    response = prompt_option(color(f"Add {section} section to config?", "yellow"), y="yes", n="no")
                    if response == "y":
                        config.add_section(section)
                        dirty = True
                        
                        clear(after=banner)
                        print(color("Section was successfully added!", "green"))
                    
                elif len(keys) == 3:
                    section = keys[0]
                    key = keys[1]
                    value = keys[2]
                    
                    response = prompt_option(color(f"Add {value} to {key}:{section}?", "yellow"), y="yes", n="no")
                    if response == "y":
                        if section not in config.sections():
                            config.add_section(section)
                            
                        config.set(section, key, value)
                        dirty = True
                        
                        clear(after=banner)
                        print(color("Value was successfully added!", "green"))
                
                else:
                    print(color("Error: Invalid command!", "red"), str(command))
                    
                   
                
            except Exception as e:
                print(e)
                print(color("Error: Invalid command!", "red"))
           
        elif command.startswith("rm"):
            try:
                keys = command.split(" ")[1:]
                
                if len(keys) == 1:
                    section = keys[0]
                    
                    response = prompt_option(color(f"Remove {section} section from config?", "yellow") + f'\n{color("Warning: Removing section will discard of all key-value pairs", "red")}', y="yes", n="no")
                    if response == "y":
                        config.remove_section(section)
                        dirty = True
                        
                        clear(after=banner)
                        print(color("Section was successfully removed!", "green"))
                    
                elif len(keys) == 2:
                    section = keys[0]
                    key = keys[1]
                    
                    response = prompt_option(color(f"Remove {key}:{section}?", "yellow"), y="yes", n="no")
                    if response == "y":
                        config.remove_option(section, key)
                        dirty = True
                        
                        if len(config[section].items()) == 0:
                            config.remove_section(section)
                        
                        clear(after=banner)
                        print(color("Key was successfully removed!", "green"))
                
                else:
                    print(color("Error: Invalid command!", "red"), str(command))
                    
            except Exception as e:
                print(e)
                print(color("Error: Invalid command!", "red"), str(command))
                
        elif command == "gen":
            new_token = True
            response = prompt_option(color("Warning: Changing validation keys on the fly may cause unintended behaviour. Be very careful when you make these changes.\n", "red") + color("Generate validation key?", "yellow"), y="yes", n="no")
            if response == "y":
                clear(after=banner)
                
                import pis.utils.integrity as integrity
                
                pfk = None
                
                if config.has_section("validation") and os.path.exists(conf.ENC_PATH):
                    print(color("Warning: Validation uses encrypted storage. Enter the current password on existing validation key.", "red"))
                    
                    new_token = False
                    pfk = hashlib.sha256(prompt_password("Enter password: ").encode()).digest()
                    k, _ = integrity.load(conf.ENC_PATH, pfk.hex())
                   
                    if not k:
                        print(color("Error: Verification failed: Invalid password!", "red"))
                        print("<any key to abort>")
                        getch()
                        break
                    
                    response = prompt_option("Change password?", y="yes", n="no")
                    if response == "y":
                        new_token = True
                            
                if new_token:
                    clear(after=banner)
                    print(color("Warning: This action will replace password token on config file. PASSWORD MUST BE SAME AS ONE USED BY THE APPLICATION.", "red"))
                    pfk = prompt_confirmpassword()
                        
                clear()
                generate_validation_keys(pfk, config, integrity, after=banner)
                
                
            
        elif command == "help" or command == "clear":
            clear(after=banner)
        elif command == "ls":
            print(tabulate([[f'<Section {section}>', k] for section in config.sections() for k, v in config[section].items()]))
        else:
            print(color("Error: Unknown command was given!", "red"), str(command))

def run_uninstall_wizard(): 
    prompt_option( color("WARNING: ", "red") + color("This will uninstall Platform Information System and all of its data. \nDo you want to continue?", "yellow"), y="yes", n="no")
    import pis.install.uninstall
    print("<Press any key to finish>")
    getch()


def main():
    print(args.init)
    if args.init:
        import pis.install.postinstall as postinstall
        postinstall.install()
        return
    
    commandlist = [
        ['Command', 'Description'],
        ['display', 'create a display'],
        ['aggregator', 'create an aggregator (management node)'],
        ['config', 'edit configuration file'],
        ['uninstall', 'uninstall the application'],
        ['quit', 'exit the wizard']
    ]

    commands = [sublist[0] for sublist in commandlist]
    commandlist.append(["", ""])
    cmd = None

    os.system('tput smcup')
    
    while True:
        clear()
        print("Welcome to the Platform Information System wizard!\n")
        print_list_services()
        print(tabulate(commandlist, headers='firstrow'))
        
        cmd = prompt("wizard# ", commands)
        
        if cmd == commands[1]: run_display_wizard()
        elif cmd == commands[2]: run_aggregator_wizard(),
        elif cmd == commands[3]: run_config_wizard(),
        elif cmd == commands[4]: run_uninstall_wizard(),
        elif cmd == "quit": break
        
        
    os.system('tput rmcup')

if __name__ == "__main__":
    main()
    