from log import Log, log
import subprocess as sp
import sys
import os


if not sys.platform.startswith('linux'):
    log(Log.ERROR, "Only linux platform is supported")
    exit()
    
if os.geteuid() != 0:
    log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)}")
    exit()

sp.run("sudo python3 refresh_conf.py nginx-wordpress-conf-https".split())

if (not os.path.isfile("/etc/ssl/private/wp_cipher.key")) or (not os.path.isfile("/etc/ssl/certs/wp_cipher.crt")):
    sp.run("sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/wp_cipher.key -out /etc/ssl/certs/wp_cipher.crt".split())

    sp.run("sudo chown root:www-data /etc/ssl/private/wp_cipher.key".split())
    sp.run("sudo chmod 640 /etc/ssl/private/wp_cipher.key".split())

log(Log.INFO, "For the changes to take effect, restart nginx!")