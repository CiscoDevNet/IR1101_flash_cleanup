1. Devices are expected to have a valid IP, Username, Password and SSH protocol enabled. This approach may require a staging environment for brand new box.
2. For brownfield case, Devices are expected to have SSH protocol enabled. (Usually disabled in the production deployments, May need to enable for this operation)
3. Script DelInstalBootFiles_v10.py will return “success.txt” file, which will contain the list of devices where the .pkg files have been deleted.
4. To Run the python script ,following packages needs to be installed,
      netmiko 2.3.3
       textfsm 0.4.1
5. Router details to be updated in the routers.txt
    Host,Username,Password,Device Type
  Sample:
   10.104.188.149,admin,Sgbu123!,cisco_xe
   10.104.188.183,admin,Sgbu123!,cisco_ios

Procedure to run the python script:
pip install netmiko==2.3.3 --ignore-installed PyYAML
pip install --upgrade textfsm==0.4.1
pip show netmiko; pip show textfsm
Update the IP, username and password in routers.txt
To execute the script, python3 DelInstalBootFiles_v10.py
