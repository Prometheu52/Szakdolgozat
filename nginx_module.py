import subprocess as sp
from log import log, Log
import sys


def print_usage():
    log(Log.ERROR, f"Wrong input arguments\nUsage:\npython {__file__}.py <arg>\n\targ:\n\t-i -> install\n\t-u -> uninstall\n\t-p -> purge (completely removes the application including config files)")


if __name__ == '__main__':
    if not sys.platform.startswith('linux'):
        log(Log.ERROR, "Only linux platform is supported")
        exit(1)
    
    try:
        action = sys.argv[1]
    except:
        print_usage()
        exit()

    match action:
        case "-i":
            sp.run(["sudo", "apt", "install", "nginx", "-y"])
        case "-u":
            sp.run(["sudo", "systemctl", "stop", "nginx"])
            sp.run(["sudo", "apt", "remove", "nginx", "nginx-common", "nginx-core"])
        case "-p":
            sp.run(["sudo", "systemctl", "stop", "nginx"])
            sp.run(["sudo", "apt", "purge", "nginx", "nginx-common", "nginx-core"])
            sp.run(["sudo", "apt", "autoremove"])
            sp.run(["sudo", "apt", "autoclean"])
        case other:
            print_usage()
            exit()
