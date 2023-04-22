from log import Log, log
import subprocess as sp
import socket
import sys
import os

def is_online():
    try:
        # Google DNS resolver
        soc = socket.create_connection(("8.8.8.8", 53))
        soc.close()
        return True
    except OSError:
        pass
    return False

def connect_to_mysql(user, host):
    message = "Please enter MySQL root password"
    while True:
        for i in range(3):
            try:
                log(Log.INFO, message)
                password = getpass.getpass("Enter password: ")
                conn = mysql.connector.connect(
                    user=user,
                    host=host,
                    consume_results=True,
                    password=password,)
                print("Connected to database!")
                return conn
            except mysql.connector.Error as e:
                print("Error: ", e)
        log(Log.WARN, "Failed to connect to database after 3 attempts.")
        message = "Please provide the MySQL root password to continue setup"

def confirm_input(text):
    while True:
        inp = input(text)
        answ = input(f"Confirm? ({inp}) y/n: ").strip().lower()
        if answ == "y":
            return inp

def create_passwd() -> str:
    while True:
        first = getpass.getpass("Account password: ")
        second = getpass.getpass("Confirm password: ")
        if first == second:
            return first
        log(Log.INFO, "Passwords does not macth! Try again!")
    
def clear():
    _ = sp.call('clear')

if not is_online():
    log(Log.ERROR, "The installation requieres internet connection. Please check your internet connection!")
    exit()

if not sys.platform.lower().startswith('linux'):
    log(Log.ERROR, "Only linux platform is supported!")
    exit()

if os.geteuid() != 0:
    log(Log.ERROR, f"Run with sudo!\nComand: sudo python3 {os.path.relpath(__file__)}")
    exit()

# General updates
log(Log.INFO, "updating system (this might take some time)...")
sp.run("sudo apt-get -qq update -y".split(" "))
sp.run("sudo apt-get -qq upgrade -y".split(" "))
sp.run("sudo apt-get -qq dist-upgrade -y".split(" "))
clear()

# Dependency handling
log(Log.INFO, "Downloading python modules...")
sp.run(["sudo", "apt-get", "-qq", "install", "python3-pip", "-y"])
sp.run(["pip", "install", "-r", "requirements.txt"])
clear()

import mysql.connector
import requests
import getpass


# Install requiered softwares
log(Log.INFO, "Downloading software packages...")
sp.run(["python3", "nginx_module.py", "-i"])
sp.run(["python3", "mysql_module.py", "-i"])
sp.run(["python3", "php_module.py"])
sp.run(["python3", "wordpress_module.py"])

# Configure nginx
sp.run(["sudo", "service", "nginx", "stop"])
sp.run("sudo rm /var/www/html/index.nginx-debian.html".split(" "))

sp.run("sudo python3 refresh_conf.py".split(" "))
clear()

# Configure mysql
log(Log.INFO, "Executing external third party setup tool...")
log(Log.INFO, "Default password for ROOT is 'root'")
sp.run(["sudo", "mysql", "--execute=ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'root';FLUSH PRIVILEGES;"])
while True:
    try:
        sp.run(["mysql_secure_installation"], check=True)
        break
    except:
        log(Log.INFO, "Default password for ROOT is 'root'")

mydb = connect_to_mysql("root", "localhost")
wp_database = "wordpress_database"
wp_acc_name, wp_acc_passwd = (None, None)

log(Log.INFO, "Please, create login credentials for the MySQL WordPress database account!")
wp_acc_name = confirm_input("Account name: ")
wp_acc_passwd = create_passwd()

mycursor = mydb.cursor()
mycursor.execute(f"CREATE DATABASE {wp_database} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
mycursor.execute(f"CREATE USER '{wp_acc_name}'@'localhost' IDENTIFIED WITH caching_sha2_password BY '{wp_acc_passwd}'")
mycursor.execute(f"GRANT ALL PRIVILEGES ON {wp_database}.* TO '{wp_acc_name}'@'localhost'")

mydb.close()
clear()

# Configure wordpress
wp_folder_dir = "/var/www/html/wordpress"
sp.run(f"sudo mv {wp_folder_dir}/wp-config-sample.php {wp_folder_dir}/wp-config.php".split(" "))

original = open(wp_folder_dir + "/wp-config.php", "r")
tmp = open("/tmp/wp-tmp-conf", "w")

url = 'https://api.wordpress.org/secret-key/1.1/salt/'
response = requests.get(url)
salts = response.text.splitlines(True)

if response.status_code != 200:
    print("[WARNING] An error occurred when retreaving salt: ", response.status_code)
    print("[INFO] Skipping writing salt...")
    for line in original.readlines():
        match line.strip():
            case "define( 'DB_NAME', 'database_name_here' );":
                tmp.write(f"define( 'DB_NAME', '{wp_database}' );")
            case "define( 'DB_USER', 'username_here' );":
                tmp.write(f"define( 'DB_USER', '{wp_acc_name}' );")
            case "define( 'DB_PASSWORD', 'password_here' );":
                tmp.write(f"define( 'DB_PASSWORD', '{wp_acc_passwd}' );")
            case other:
                tmp.write(line)
    tmp.close()
    original.close()
        
    original = open(wp_folder_dir + "/wp-config.php", "w")
    tmp = open("/tmp/wp-tmp-conf", "r")

    original.write(tmp.read())

    tmp.close()
    original.close()
else:
    for line in original.readlines():
        match line.strip():
            case "define( 'DB_NAME', 'database_name_here' );":
                tmp.write(f"define( 'DB_NAME', '{wp_database}' );")
            case "define( 'DB_USER', 'username_here' );":
                tmp.write(f"define( 'DB_USER', '{wp_acc_name}' );")
            case "define( 'DB_PASSWORD', 'password_here' );":
                tmp.write(f"define( 'DB_PASSWORD', '{wp_acc_passwd}' );")
            case "define( 'AUTH_KEY',         'put your unique phrase here' );":
                tmp.write(salts[0])
            case "define( 'SECURE_AUTH_KEY',  'put your unique phrase here' );":
                tmp.write(salts[1])
            case "define( 'LOGGED_IN_KEY',    'put your unique phrase here' );":
                tmp.write(salts[2])
            case "define( 'NONCE_KEY',        'put your unique phrase here' );":
                tmp.write(salts[3])
            case "define( 'AUTH_SALT',        'put your unique phrase here' );":
                tmp.write(salts[4])
            case "define( 'SECURE_AUTH_SALT', 'put your unique phrase here' );":
                tmp.write(salts[5])
            case "define( 'LOGGED_IN_SALT',   'put your unique phrase here' );":
                tmp.write(salts[6])
            case "define( 'NONCE_SALT',       'put your unique phrase here' );":
                tmp.write(salts[7])
            case other:
                tmp.write(line)

    tmp.close()
    original.close()

    original = open(wp_folder_dir + "/wp-config.php", "w")
    tmp = open("/tmp/wp-tmp-conf", "r")

    original.write(tmp.read())

    tmp.close()
    original.close()

log(Log.INFO, "LEMP installation is finished!")
log(Log.INFO, "To start the server run the following: sudo service nginx start")

# sudo usermod -a -G vboxsf all-in-one
