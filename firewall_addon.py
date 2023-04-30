from log import Log, log
from enum import Enum
import subprocess as sp
import sys
import os

class Action(Enum):
    ALLOW = 0
    DENY = 1

def port_action(action: Action, ports: list):
    for port in ports:
        if port.lower() == "all":
            match action:
                case Action.ALLOW:
                    if input("Opening ALL ports, are you sure? (Yes/n): ") == "Yes":
                        sp.run("sudo ufw allow 1:65535/tcp".split())
                    return
                case Action.DENY:
                    sp.run("sudo ufw deny 1:65535/tcp".split())
                    return

        try:
            port = int(port)
            if port > 65_535:
                log(Log.WARN, f"Invalid port value (max: 65535): {port}")
                raise "Invalid port value"
        except:
            log(Log.WARN, f"Skipping \'{'DENY' if action == Action.DENY else 'ALLOW'}\' rule for \'{port}\', Reason: Invalid port number")
            continue

        match action:
            case Action.ALLOW:
                sp.run(f"sudo ufw allow {port}/tcp".split())
            case Action.DENY:
                sp.run(f"sudo ufw deny {port}/tcp".split())


if __name__ == "__main__":
    if not sys.platform.startswith('linux'):
        log(Log.ERROR, "Only linux platform is supported")
        exit()

    if os.geteuid() != 0:
        log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)} <args>")
        exit()

    # Is UFW enabled?
    if sp.run(['sudo', 'ufw', 'status'], stdout=sp.PIPE).stdout.decode('utf-8').split(":")[1].strip() == "inactive":
        log(Log.ERROR, f"The firewall is inactive, enable firewall before running this")
        log(Log.INFO, "Hint - Run the following to enable firewall: sudo ufw enable")
        exit()

    # sudo firewall_interface.py -d:80,90,123 
    # sudo firewall_interface.py -a:80,90,123 

    if len(sys.argv) == 2:
        args = sys.argv[1].split(":")
        cmd = args[0].lower()
        ports = args[1].split(",")
        match cmd:
            case "deny":
                port_action(Action.DENY, ports)
            case "allow":
                port_action(Action.ALLOW, ports)
            case "-d":
                port_action(Action.DENY, ports)
            case "-a":
                port_action(Action.ALLOW, ports)
            case other:
                log(Log.ERROR, "Parsing error - Check input parameters")  
    else:
        log(Log.ERROR, "Parsing error - Check input parameters")