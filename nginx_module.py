from log import log, Log
import subprocess as sp
import sys
import os


def print_usage():
    log(Log.ERROR, f"Wrong input arguments\nUsage:\npython {os.path.relpath(__file__)}.py <arg>\n\targ:\n\t-i -> install\n\t-u -> uninstall\n\t-p -> purge (completely removes the application including config files)")

def install():
    sp.run(["sudo", "apt-get", "-qq", "install", "nginx", "-y"])

def uninstall():
    sp.run(["sudo", "systemctl", "stop", "nginx"])
    sp.run(["sudo", "apt", "remove", "nginx", "nginx-common", "nginx-core"])

def purge():
    sp.run(["sudo", "systemctl", "stop", "nginx"])
    sp.run(["sudo", "apt", "purge", "nginx", "nginx-common", "nginx-core"])
    sp.run(["sudo", "apt", "autoremove"])
    sp.run(["sudo", "apt", "autoclean"])


if __name__ == '__main__':
    if not sys.platform.startswith('linux'):
        log(Log.ERROR, "Only linux platform is supported")
        exit()
    
    if os.geteuid() != 0:
        log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)}")
        exit()

    try:
        action = sys.argv[1]
    except:
        print_usage()
        exit()

    match action:
        case "-i":
            install()
        case "-u":
            uninstall()
        case "-p":
            purge()
        case other:
            print_usage()
            exit()
