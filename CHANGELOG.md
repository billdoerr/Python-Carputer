# Changelog
All notable changes to this Python Carputer project will be documented in this file.


## [Unreleased]
### v1.x (NOT STARTED)
#### Added
#### Changed
#### Removed


## [Unreleased]
### v1.x (NOT STARTED)
#### Added
#### Changed
#### Removed

## [Released]
### v1.0 (17May2019)
#### Added
- [x]  listen_for_shutdown.py - Python script that listens for button press and after short period, ~5 seconds, will issue a shutdown command to slave and master nodes.
        Bash shell script also included so that this starts upon boot-up.

		• sudo apt install python3-paramiko     < install required ssh package
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
		

