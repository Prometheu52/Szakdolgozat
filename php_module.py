from log import log, Log
import subprocess as sp
import sys
import os

def install():
    sp.run(["sudo", "apt-get", "-qq", "install", "php-fpm", "-y"])
    sp.run(["sudo", "apt-get", "-qq", "install", "php-mysql", "-y"])

if __name__ == '__main__':
    if not sys.platform.startswith('linux'):
        log(Log.ERROR, "Only linux platform is supported")
        exit()

    if os.geteuid() != 0:
        log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)}")
        exit()
    
    install()
