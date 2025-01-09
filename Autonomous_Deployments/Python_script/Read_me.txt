1. Devices are expected to have a valid IP, Username, Password and SSH protocol enabled.
2. Devices are expected to have SSH protocol enabled. to login to the routers.
3.  To Run the python script, following packages needs to be installed,
      netmiko 2.3.3
      textfsm 0.4.1

4. Need to create routers.txt file and router details need to be updated as below.
   Host,Username,Password,Device Type
  Sample:
   10.104.188.149,admin,Sgbu123!,cisco_xe
   10.104.188.183,admin,Sgbu123!,cisco_ios

5. FindPkgFiles_v5.py script creates "routers_with_pkg.txt" and "failed_connections.txt" files, user needs to delete these files for every re-run.
FindPkgFiles_v5.py uses routers.txt as input.

6. DelInstalBootFiles_v9.py script will delete .pkg and .conf files from flash: if router is booted with .bin (bundle boot) and uses "routers_with_pkg.txt" as input.

7. DelInstalBootFiles_v9.py script will return a file named “success.txt”, which will contain a list of devices where the .pkg and .conf files have been deleted.

Procedure to run the python script:
pip install netmiko==2.3.3 --ignore-installed PyYAML
pip install --upgrade textfsm==0.4.1
pip show netmiko; pip show textfsm
Update the IP, username and password in routers.txt


To run# python3 FindPkgFiles_v5.py
      # python3 DelInstalBootFiles_v9.py
