import subprocess as sp
from log import log, Log
import sys

if __name__ == '__main__':
    if not sys.platform.startswith('linux'):
        log(Log.ERROR, "Only linux platform is supported")
        exit()
    
    sp.run(["sudo", "apt", "install", "php-fpm", "-y"])
    sp.run(["sudo", "apt-get", "install", "php-mysql", "-y"])
