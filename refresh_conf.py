import subprocess as sp
from log import log, Log
import sys
import os

if not sys.platform.lower().startswith('linux'):
    log(Log.ERROR, "Only linux platform is supported!")
    exit()

if os.geteuid() != 0:
    log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)}")
    exit()

def usage():
    log(Log.ERROR, f"Wrong input arguments\nUsage:\nsudo python3 {os.path.relpath(__file__)} <optional:path>")

def change_config(path: str):
    conf_file = open("/etc/nginx/sites-available/wordpress.conf", "w")
    conf = open(path, "r")
    conf_file.write(conf.read())


match len(sys.argv):
    case 1:
        change_config("nginx-wordpress-conf")
    case 2:
        match sys.argv[2]:
            case "help":
                log(Log.INFO, "This script changes the contents of '/etc/nginx/sites-available/wordpress.conf' to the specified file's contents in arguments. \nIf no argument was provided the default file is 'nginx-wordpress-conf'")
            case other:
                change_config(sys.argv[2])
    case other:
        usage()
        exit()

if not os.path.isfile("/etc/nginx/sites-enabled"):
    sp.run(["sudo", "ln", "-s", "/etc/nginx/sites-available/wordpress.conf", "/etc/nginx/sites-enabled"])

if os.path.isfile("/etc/nginx/sites-enabled/default"):
    sp.run(["sudo", "unlink", "/etc/nginx/sites-enabled/default"])

log(Log.INFO, "For the changes to take effect, restart nginx!")