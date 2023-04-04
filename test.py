from log import log, Log
import subprocess as sp
import getpass

import mysql.connector
from mysql.connector import errorcode

# General updates
# sp.run("sudo apt update -y".split(" "))
# sp.run("sudo apt upgrade -y".split(" "))
# sp.run("sudo apt dist-upgrade".split(" "))

# Install requiered softwares
# sp.run(["sudo", "apt-get", "install", "python3-pip", "-y"])
# sp.run(["pip", "install", "-r", "requirements.txt"])
# sp.run(["python3", "mysql_module.py", "-i"])

if __name__ == '__main__':
  def connect_to_mysql(user, host):
    log(Log.INFO, "Please enter root password")
    for i in range(3):
      try:
        password = getpass.getpass("Enter password: ")
        conn = mysql.connector.connect(
          user=user,
          host=host,
          consume_results=True,
          password=password)
        print("Connected to database!")
        return conn
      except mysql.connector.Error as e:
          print("Error: ", e)
    log(Log.WARN, "Failed to connect to database after 3 attempts.")
    return None
  
  def create_passwd() -> str:
    while True:
      first = getpass.getpass("Account password: ")
      second = getpass.getpass("Confirm password: ")
      if first == second:
        break
      log(Log.INFO, "Passwords does not macth! Try again!")
    
    return first



  mydb = connect_to_mysql("root", "localhost")
  if mydb is not None:
    mycursor = mydb.cursor()
    # mycursor.execute(f"CREATE DATABASE {wp_database} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    # mycursor.execute(f"CREATE USER '{wp_acc_name}'@'localhost' IDENTIFIED WITH caching_sha2_password BY '{wp_acc_passwd}'")
    # mycursor.execute(f"CREATE USER '{wp_acc_name}'@'localhost' IDENTIFIED BY '{wp_acc_passwd}'")
    # mycursor.execute(f"GRANT ALL PRIVILEGES ON {wp_database}.* TO '{wp_acc_name}'@'localhost'")
    mycursor.execute("SHOW DATABASES")
    databases = mycursor.fetchall()

    mycursor.execute("SELECT user FROM mysql.user")
    users = mycursor.fetchall()
    mydb.close()
  else:
    log(Log.WARN, "Skipping table and user creation...")
  log(Log.INFO, "Users:");
  for row in users:
    print("  ", row[0])
  log(Log.INFO, "Databases:");
  for row in databases:
    print("  ", row[0])
