from log import Log, log
import subprocess as sp
import sys
import os

if not sys.platform.startswith('linux'):
    log(Log.ERROR, "Only linux platform is supported")
    exit()

if os.geteuid() != 0:
    log(Log.ERROR, "Run with sudo!\nComand: sudo python3 LEMP.py")
    exit()

log(Log.WARN, "This will remove EVERYTHING! \nConfiguration and program files regarding nginx, mysql and wordpress; and ALL content in the wordpress folder.")
r_u_sure = input("Do you want to proceed? Yes/n: ").strip()
if r_u_sure != "Yes":
    log(Log.INFO, "Exiting..")
    exit()

import nginx_module
import mysql_module

nginx_module.purge()
mysql_module.purge()
sp.run("sudo rm -rf /var/www/html/wordpress".split(" "))

# Remove SSL certs?
# sudo rm "/etc/ssl/private/wp_cipher.key" && sudo rm "/etc/ssl/certs/wp_cipher.crt"
