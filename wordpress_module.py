import subprocess as sp
import sys
import os
from log import Log, log


if __name__ == '__main__':
    if not sys.platform.startswith('linux'):
        log(Log.ERROR, "Only linux platform is supported")
        exit()

    if len(sys.argv) != 1:
        directory = sys.argv[1]

        sp.run(["sudo", "wget", "-P", f"{directory}", "https://wordpress.org/latest.tar.gz"])
        sp.run(["sudo", "tar", "-xzf", f"{directory}/latest.tar.gz", "-C", f"{directory}"])
        sp.run(["sudo", "rm", f"{directory}/latest.tar.gz"])
    else:
        if os.geteuid() != 0:
            log(Log.ERROR, "Run with sudo!\nComand: sudo python3 LEMP.py")
            exit()
        
        directory = "/var/www/html"
        if not os.path.exists(directory):
            sp.run(["sudo", "mkdir", "-p", f"{directory}"])

        sp.run(["sudo", "wget", "-P", f"{directory}", "https://wordpress.org/latest.tar.gz"])
        sp.run(["sudo", "tar", "-xzf", f"{directory}/latest.tar.gz", "-C", f"{directory}"])
        sp.run(["sudo", "rm", f"{directory}/latest.tar.gz"])

