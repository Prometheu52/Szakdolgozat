from log import log, Log
import subprocess as sp
import sys

def print_usage():
    log(Log.ERROR, f"Wrong input arguments\nUsage:\npython {os.path.relpath(__file__)} <arg>\n\targ:\n\t-i -> install\n\t-u -> uninstall\n\t-p -> purge (completely removes the application including config files)")

if __name__ == '__main__':
    if not sys.platform.startswith('linux'):
        log(Log.ERROR, "Only linux platform is supported")
        exit()

    try:
        action = sys.argv[1]
    except:
        print_usage()
        exit()

    match action:
        case "-i":
            sp.run(["sudo", "apt-get", "-qq", "install", "mysql-server", "-y"])
        case "-u":
            sp.run(["sudo", "systemctl", "stop", "mysql"])
            sp.run(["sudo", "apt", "remove", "mysql*"])
        case "-p":
            sp.run(["sudo", "systemctl", "stop", "mysql"])
            sp.run(["sudo", "apt", "purge", "mysql*"])
            sp.run(["sudo", "apt", "autoremove", "-y"])
            sp.run(["sudo", "apt", "autoclean", "-y"])
            sp.run("sudo rm -rf /etc/mysql".split(" "))
            sp.run("sudo rm -rf /var/lib/mysql".split(" "))
        case other:
            print_usage()
            exit(1)


# sudo mysql_secure_installation
# sudo mysql --execute="ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'testpass';FLUSH PRIVILEGES;"

