import subprocess as sp
import sys
import os
from log import Log, log


if __name__ == '__main__':
    if not sys.platform.startswith('linux'):
        log(Log.ERROR, "Only linux platform is supported")
        exit()

    if os.geteuid() != 0:
        log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)}")
        exit()

    directory = sys.argv[1] if len(sys.argv) == 2 else "/var/www/html"

    sp.run(["sudo", "wget", "-P", f"{directory}", "https://wordpress.org/latest.tar.gz"])
    sp.run(["sudo", "tar", "-xzf", f"{directory}/latest.tar.gz", "-C", f"{directory}"])
    sp.run(["sudo", "rm", f"{directory}/latest.tar.gz"])


