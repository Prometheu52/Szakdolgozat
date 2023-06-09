from log import *
import pw
import subprocess as sp
import getpass
import sys
import os


def change_passwd(user: str):
    new_passwd = pw.create_passwd(pw.ask(), prompt="New password: ")
    sp.run(["sudo", "usermod", "-p", f"$(openssl passwd -6 {new_passwd})", f"{user}"])

if __name__ == '__main__':
    log(Log.ERROR, "This addon is under maintanance! Quitting application...")
    exit()
    
    if not sys.platform.startswith('linux'):
        log(Log.ERROR, "Only linux platform is supported")
        exit()

    if os.geteuid() != 0:
        log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)}")
        exit()

    admin_user = "productowner"
    running_user = getpass.getuser()

    if admin_user != running_user:
        log(Log.WARN, f"This action will change \'{running_user}\' user\'s password rather than the \'{admin_user}\'")
        match input("Do you wish to continue? (y/n): ").strip().lower():
            case "y":
                log(Log.INFO, f"Changing password for \'{getpass.getuser()}\'")
                change_passwd(getpass.getuser())
            case other:
                log(Log.INFO, f"Changing password for \'{admin_user}\'")
                change_passwd(admin_user)
    else:
        log(Log.INFO, f"Changing password for \'{admin_user}\'")
        change_passwd(admin_user)