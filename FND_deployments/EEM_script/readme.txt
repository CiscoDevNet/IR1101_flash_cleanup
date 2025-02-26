1. For Greenfield On-boarding [PnP]:
Step:1 Navigate to Config -> Tunnel Provisioning -> Router Bootstrap Configuration.
Step:2 Update the existing bootstrap config with the below applet [DeleteInstallBootFiles].
Step:3 Start the PnP process.

2. For Brownfield scenario:
Step:1 Navigate to Config -> Device Configuration -> Groups -> Edit configuration Template
Step:2 Update the existing config push template with the below applet [DeleteInstallBootFiles].
Step:3 Click on Push Configuration -> Select "Push Router  configuration" from the drop box and Submit
Note: Devices are expected to rollback and re-register

3. Countdown timer should be set to 2 seconds in the below EEM script. 
Changing the countdown timer may increase the script execution time, which may result in updating the applet in the before-tunnel-config file.
