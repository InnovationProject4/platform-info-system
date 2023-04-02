import  os, sys, termios, tty, shutil, subprocess, re
import stationCodes
from tabulate import tabulate


'''
Installation wizard for passenger-information-system displays. 
Directs the user to easily manage systemd services.
'''
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

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)  # or tty.setraw(fd) for raw mode.
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, old)

def clear(after=None):
    os.system("clear")
    #os.system("cls")
    if after is not None:
        after()

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
        
        if key == "\x1b[A" or key == "A":  # Up arrow
            selected = (selected - 1) % selection_max
        elif key == "\x1b[B" or key == "B":  # Down arrow
            selected = (selected + 1) % selection_max
            
        # Exit on enter
        elif key == "\n":
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
        if ch == " ":
            if options:
                if options[cursor_pos] in selected:
                    selected.remove(options[cursor_pos])
                else:
                    if len(selected) < limit:
                        selected.append(options[cursor_pos])
        elif ch == "\r":
            if selected:
                return selected
        elif ch == "\n":
            if selected:
                return selected
        elif ch == "\x1b":
            getch() # Consume the second byte of an arrow key sequence
            ch = getch()
            if ch == "A":
                cursor_pos = max(0, cursor_pos - 1)
                if cursor_pos < scroll_offset:
                    scroll_offset = cursor_pos
            elif ch == "B":
                cursor_pos = min(len(options) - 1, cursor_pos + 1)
                if cursor_pos >= scroll_offset + offset:
                    scroll_offset = cursor_pos - (offset - 1)
                    
        elif ch == "\x7f":
            queryString = queryString[:-1] # Remove latest letter on backspace
            options = fuzzy_search(queryString, checklist)
        else:
            queryString += ch
            options = fuzzy_search(queryString, checklist)
        print(ch)
    
        
def print_list_services():
    '''get a list of information system services that are active'''
    services = subprocess.check_output(['systemctl', 'list-units', '--type=service', '--state=active', '--no-legend', '--no-pager', '--all', '*.pids.service*'], encoding='utf-8')
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
        os.system("clear")
        banner()
        platform= input("Type platform: ")
        
    station = (prompt_checklist("Select railway station(s) you want to listen for. Press SPACE to select: ", [' '.join(t) for t in stationCodes.names], after=banner, limit=1))[0].split(" ")[0]
    
    transit = prompt_radioGroup("Select transit type: ", ['departures', 'arrivals', "None"], after=banner)
    transport = prompt_radioGroup("Select transport type: ", ['commuter', 'long_distance', "None"], after=banner)
    
    os.system("clear")
    banner()
    response = prompt_option("Create display service file?", y="yes", n="no")
    if response == "y":
        service_file = create_service_file(f'{view}_{station}.pids', f'Display service for {view} at {station} platform {platform}', "display_client.py", build_args_string())
        
        response = prompt_option("Install display service?", y="yes", n="no")
        if response == "y":
            install_service(service_file)
        
    elif response == "n":
        response = prompt_option("Run display with python now?", y="yes", n="no")
        if response == "y":
            pass
        
    response = prompt_option("continue?", y="yes", n="no")
    
    
def run_aggregator_wizard():
    stations = []
    
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
            ["-s, -station", "one or multiple station shortCodes: ex. HSL (Helsinki Asema)"]
        ]))
        print(f'{color("-s", "light_blue")} \033[92m{build_args_string()}\033[0m')
        
        
    selected = (prompt_checklist("Select railway station(s) you want to listen for. Press SPACE to select: ", [' '.join(t) for t in stationCodes.names], after=banner))
    for station in selected:
        stations.append(station.split(" ")[0])
    
    os.system("clear")
    banner()
    response = prompt_option("Create display service file?", y="yes", n="no")
    if response == "y":
        service_file = create_service_file(f'aggregator.pids', f'Data aggregator for platform-info-system', "aggregator.py", build_args_string("-s "))
        
        response = prompt_option("Install aggregation service?", y="yes", n="no")
        if response == "y":
            install_service(service_file)
        
    elif response == "n":
        response = prompt_option("Run aggregator with python now?", y="yes", n="no")
        if response == "y":
            pass
        

commandlist = [
    ['Command', 'Description'],
    ['display', 'create a display'],
    ['aggregator', 'create an aggregator (management node)'],
    ['quit', 'exit the wizard']
]

commands = [sublist[0] for sublist in commandlist]

commandlist.append(["", ""])
cmd = None



def main():
    os.system('tput smcup')
    
    while True:
        os.system('clear')
        print("Welcome to the display creation wizard!\n")
        print_list_services()
        print(tabulate(commandlist, headers='firstrow'))
        
        cmd = prompt("wizard# ", commands)
        
        if cmd == commands[1]: run_display_wizard()
        elif cmd == commands[2]: run_aggregator_wizard()
        elif cmd == "quit": break
        


    
    os.system('tput rmcup')


if __name__ == "__main__":
    main()
    