import subprocess as sp
from log import log, Log
import sys

if not sys.platform.startswith('linux'):
    log(Log.ERROR, "Only linux platform is supported")
    exit()

conf_file = open("/etc/nginx/sites-available/wordpress.conf", "w")
conf = open("wordpress-conf", "r")
conf_file.write(conf.read())

# Cerate symlink
sp.run(["sudo", "ln", "-s", "/etc/nginx/sites-available/wordpress.conf", "/etc/nginx/sites-enabled"])
sp.run(["sudo", "unlink", "/etc/nginx/sites-enabled/default"])

# Restart nginx
sp.run(["sudo", "service", "nginx", "restart"])
