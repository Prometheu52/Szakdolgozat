from log import Log, log
import subprocess as sp
import socket
import sys
import os


def usage():
    log(Log.INFO, "Downloads the latest version of WordPress in the specified path in args. The default value is '/var/www/html'")
    log(Log.ERROR, f"Wrong input arguments\nUsage:\nsudo python3 {os.path.relpath(__file__)} <optional:path>")

def is_online():
    try:
        # Google DNS resolver
        soc = socket.create_connection(("8.8.8.8", 53))
        soc.close()
        return True
    except OSError:
        pass
    return False

# "/var/www/html"
def install(directory="/var/www/html"):
    sp.run(["sudo", "wget", "-P", f"{directory}", "https://wordpress.org/latest.tar.gz"])
    sp.run(["sudo", "tar", "-xzf", f"{directory}/latest.tar.gz", "-C", f"{directory}"])
    sp.run(["sudo", "rm", f"{directory}/latest.tar.gz"])

if __name__ == '__main__':
    if not sys.platform.startswith('linux'):
        log(Log.ERROR, "Only linux platform is supported")
        exit()

    if os.geteuid() != 0:
        log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)}")
        exit()
    
    if not is_online():
        log(Log.ERROR, "The installation requieres internet connection. Please check your internet connection!")
        exit()

    match len(sys.argv):
        case 1:
            install()
        case 2:
            directory = sys.argv[1]
            if os.path.isdir(directory):
                install(directory)
            else:
                log(Log.ERROR, "Path does not exist!")
        case other:
            usage()
            exit()


