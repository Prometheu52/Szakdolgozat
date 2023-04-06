# Automation tool to setup a LEMP serven on Linux Mint Cinnamon edition

**This is a highly volatile project and, not production ready!**

The script assumes to be run in a **VM** enviroment under **sudo** privileges.
In current form it is not setup to work outside localhost! But the ability to do so is not restricted. You have full controll over the configuration files after the installation. 

Make sure that the to be installed softwares are not present on the target machine because, this completely rewirites any previous configurations you have! Alternatively you can change the corresponding conf files.

The files that ends with '_module.py' can be run independently and only does what it's name suggest; there are usage instructions with every one of them.

## Installation:
Run the following in the terminal: 
```console
$ sudo <your_python_version> LEMP.py
```
Follow the instructions during installation!

## Uninstallation:
Run the following in the terminal: 
```console
$ sudo <your_python_version> UNINSTALL_LEMP.py
```

**Please for the love of god! If you will use this in production, use strong passwords!!!**
