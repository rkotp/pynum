# PYNUM: Python Based Network Users Management
### Description
What's Pynum? Pynum is the acronym for Python Based Network Users Management. As the acronym tells, this tool will help us to handle the users connected to a certain network. It is developed in Python in its third version. It has been developed and designed following two guidelines:
* Easy-to-use: It has been launched with an easy web interface that lets everybody use it.
* Developer-friendly: It is all well commented and documented in order to help developers to add more features or to correct bugs. If you edit the code, we would appreciate it if you send it to us to add the improvements to the project.
### Requirements
The source code has been developed over Python 3.8, so it is strictly mandatory. It has not been tested on python 3.9.
The folowing modules are mandatory. You could install them with the command `pip3 install xxxxx`, where `xxxxx` is each one of the following modules. Otherwise, in the installation method (step 3) another (and easier) method is given. The required modules are:
- Scapy
- Flask
- ipaddress
- netaddr
- termcolor
### Installation
Donwload, install and run pynum with the following commands:
1. Download this git
`git clone https://github.com/rkotp/pynum.git`
2. Access the folder downloaded
`cd pynum`
3. Install the required libraries
`sudo python3 -m pip install -r requirements.txt`
4. Run it and have fun!
`sudo python3 pynum.py`
### Usage
First you must change (or at least watch) the credentials at config.xml. Run it with the command 4 of the previous section. Access to your web explorer and navigate to http://<<ip_from_where_pynum_is_running>>:9000. If you are accessing the service from the same machine where it is running you can also access to http://localhost:9000 or http://0.0.0.0:9000. Then, type the credentials and play!
### Contact
You can contact the developer at rkotp@protonmail.com
### License
This software is licensed under GNU General Public License v3.0. You can review the full license document for more  details.
### Authors
It has been developed under th framework of a master thesis. The authors are:
* Pedro Ruben González Sánchez - Developer
* Pablo Serrano - Supervisor
