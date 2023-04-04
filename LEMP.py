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
    log(Log.INFO, "Please enter root password")
    for i in range(3):
        try:
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
    return None

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
    

if not is_online():
    log(Log.ERROR, "The installation requieres internet connection. Please check your internet connection!")
    exit()

if not sys.platform.startswith('linux'):
    log(Log.ERROR, "Only linux platform is supported!")
    exit()

if os.geteuid() != 0:
    log(Log.ERROR, "Run with sudo!\nComand: sudo python3 LEMP.py")
    exit()

# General updates
log(Log.INFO, "apt update && upgrade && dist-upgrade...")
sp.run("sudo apt update -y".split(" "))
sp.run("sudo apt upgrade -y".split(" "))
sp.run("sudo apt dist-upgrade".split(" "))

# Dependency handling
log(Log.INFO, "Downloading python modules...")
sp.run(["sudo", "apt-get", "install", "python3-pip", "-y"])
sp.run(["pip", "install", "-r", "requirements.txt"])

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
# TODO: Remove default-nginx-welcome-page.html
sp.run(["sudo", "service", "nginx", "stop"])

conf_file = open("/etc/nginx/sites-available/wordpress.conf", "w")
conf = open("wordpress-conf", "r")
conf_file.write(conf.read())

# Cerate symlink
sp.run(["sudo", "ln", "-s", "/etc/nginx/sites-available/wordpress.conf", "/etc/nginx/sites-enabled"])
sp.run(["sudo", "unlink", "/etc/nginx/sites-enabled/default"])

# Restart nginx
log(Log.INFO, "To start the web-server, later run the following: sudo service nginx start\n")

# Configure mysql
log(Log.INFO, "Default password for ROOT is 'root'")
sp.run(["sudo", "mysql", "--execute=ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'root';FLUSH PRIVILEGES;"])
sp.run(["mysql_secure_installation"])

mydb = connect_to_mysql("root", "localhost")
wp_database = "wordpress_database"
wp_acc_name, wp_acc_passwd = (None, None)
if mydb is not None:
    log(Log.INFO, "Please, create login credentials for the MySQL WordPress database account!")
    wp_acc_name = confirm_input("Account name: ")
    wp_acc_passwd = create_passwd()

    mycursor = mydb.cursor()
    mycursor.execute(f"CREATE DATABASE {wp_database} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    mycursor.execute(f"CREATE USER '{wp_acc_name}'@'localhost' IDENTIFIED WITH caching_sha2_password BY '{wp_acc_passwd}'")
    mycursor.execute(f"GRANT ALL PRIVILEGES ON {wp_database}.* TO '{wp_acc_name}'@'localhost'")

    mydb.close()
else:
    #TODO: Handle the aftemath gracefully
    log(Log.WARN, "Skipping table and user creation...")



# Configure wordpress
# Copy code from test2.py

# sudo usermod -a -G vboxsf all-in-one
