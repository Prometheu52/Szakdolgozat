from log import Log, log
import subprocess as sp


if not sys.platform.startswith('linux'):
    log(Log.ERROR, "Only linux platform is supported")
    exit()
    
if os.geteuid() != 0:
    log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)}")
    exit()