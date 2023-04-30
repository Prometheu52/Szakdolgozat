from log import Log, log
import subprocess as sp
import sys
import os


if not sys.platform.startswith('linux'):
    log(Log.ERROR, "Only linux platform is supported")
    exit()

# !!! These variables not meant to be tampered with !!! #
key_file = "/etc/ssl/private/wp_cipher.key"
crt_file = "/etc/ssl/certs/wp_cipher.crt"
conf_file = "nginx-wordpress-conf-https"

if len(sys.argv) == 2:
    log(Log.WARN, "This script takes no input arguments. ")
    log(Log.INFO, f"This script generates the neccessary RSA cipher for https signing, if these ciphers are not already present: \n\tPrivate key: {key_file}\n\tPublic key: {crt_file}")
    log(Log.INFO, "Also gives permission to the Nginx master process to read the key file.\n")

log(Log.WARN, f"This will replace the Nginx config's contents to '{conf_file}' contents.")
log(Log.WARN, "In current version there is no automated script to undo this action.")
answ = "Do you wish to continue? (y/n): "
if input(answ).strip().lower() != "y":
    exit()

if os.geteuid() != 0:
    log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)}")
    exit()

if (not os.path.isfile("/etc/ssl/private/wp_cipher.key")) or (not os.path.isfile("/etc/ssl/certs/wp_cipher.crt")):
    sp.run(f"sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout {key_file} -out {crt_file}".split())

    sp.run("sudo chown root:www-data /etc/ssl/private/wp_cipher.key".split())
    sp.run("sudo chmod 640 /etc/ssl/private/wp_cipher.key".split())

    sp.run(f"sudo python3 refresh_conf.py {conf_file}".split())

    log(Log.WARN, "This is considered a SELF-SIGNED certification. This means that the browser will give a warning when visiting the site for the first time!")
    log(Log.INFO, "Certification done!")
    exit()

log(Log.INFO, "No changes were made")
log(Log.INFO, "If you wish to load a changed version of an Nginx config, try running: sudo python3 refresh_conf.py <nginx-conf-file>")
