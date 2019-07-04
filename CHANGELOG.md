# Changelog
All notable changes to this Python Carputer project will be documented in this file.
File:  D:\Users\bdoerr\Development\Python\PycharmProjects\carputer\CHANGELOG.md


## [Unreleased]
### v1.x (NOT STARTED)
#### Added
#### Changed
#### Removed


## [Released]
### v1.1 (4Jul2019)
#### Added
#### Changed
- [x] Change version tag in listen_for_shutdown.py:  __version__ = '1.1'
- [x] listen_for_shutdown.sh:  Removed this section of code in start() function.
        # Remove log file upon start.  Used only for debugging.
        # sudo rm -f /var/log/carputer/listen_for_shutdown.log      # Addressed in python script filemode='w'
- [x] listen_for_shutdown.py:  Added "filemode='w'" in log_init(). file_handler = logging.FileHandler('/var/log/carputer/listen_for_shutdown.log', 'w')  Opens a file for writing only. Overwrites the file if the file exists. If the file does not exist, creates a new file for writing.    
- [x] listen_for_shutdown.py:  Changed log record formatting. 
- [x] listen_for_shutdown.py:  filename = '/var/lib/misc/dnsmasq.leases' does not contain ip's of nodes as expected.  Created filename = '/etc/carputer/nodes.config' which contains
                               single node '192.168.4.5' as temporary work around.  Python script changed to read the 'nodes' file instead of 'dnsmasq.leases'.
#### Removed

## [Released]
### v1.0 (17May2019)
#### Added
- [x]  listen_for_shutdown.py - Python script that listens for button press and after short period, ~5 seconds, will issue a shutdown command to slave and master nodes.
        Bash shell script also included so that this starts upon boot-up.

		• sudo apt install python3-paramiko     # install required ssh package
        
		• cd /etc/init.d
		• sudo vi listen_for_shutdown.sh
		• sudo chmod +x listen_for_shutdown.sh
		• sudo mkdir /var/log/carputer
		• cd /usr/local/bin
		• sudo vi listen_for_shutdown.py
		• sudo chmod +x listen_for_shutdown.py
		• sudo update-rc.d listen_for_shutdown.sh defaults
		• sudo reboot
		• cd /var/log/carputer/
		• ls
        • tail -f listen_for_shutdown.log
        
- [x] heartbeat.py - Python script that turns on/off led once per second to indicate that system is running.
        Bash shell script also included so that this starts upon boot-up.

		• cd /etc/init.d
		• sudo vi heartbeat.sh
		• sudo chmod +x heartbeat.sh
		• sudo mkdir /var/log/carputer
		• cd /usr/local/bin
		• sudo vi heartbeat.py
		• sudo chmod +x heartbeat.py
		• sudo update-rc.d heartbeat.sh defaults
		• sudo reboot
		• cd /var/log/carputer/
		• ls
		• tail -f heartbeat.log

#### Changed
#### Removed
		

