# Prosthetic Arm Engineering Clinic
#### Rowan University
#### Department of Electrical and Computer Engineering
#### Advisor: Dr. Rasool
#### First Commit - Fall Semester 2018 (But includes work from previous semesters never recorded on Git)

SETUP
-----
### RPi Zero W
Raspberry Pi Zero W was used as the controller for this project. Luckily, this 
version used has an on-board WiFi chip which enables SSH. Unfortunately, 
this WiFi chip cannot connect to Rowan WiFis (can probably connect to IoT engineering 
network but solution used was easier).

### MYO Band
On any computers using scripts which get data from MYO band, MyoConnect will 
be need to be installed. This essentially makes a "hub" object within python 
which is where data is retrieved from. MyoConnect is only for Windows but 
there is a Linux alternative called PyoConnect.

##### LOGIN CREDENTIALS
- Username: pi
- Password: rowanclinic
- NOTE: These are the credentials that were set at the end of the Fall 2018 
semester and can be changed by future teams. At the end of each semester 
these credentials should be updated for the next team

To connect to RPi, folloing steps must be done...
1. Have at least one group member with smart phone or usable hotspot.
2. Get SSID (name) that hotspot is set to and password used.
3. Interface with RPi in one of two ways to set WiFi connectivity settings
    - Hook up RPi to monitor and keyboard
        1. NOTE: Will need USB keyboard as well as cable with mini HDMI for RPi 
        2. Plug in mini HDMI cord to RPi and connect other end to monitor 
        3. Plug in USB keyboard to micro USB to USB adapter attached to RPi 
        4. Plug in micro USB cord to other micro USB port to power RPi 
        5. Use keyboard hotkeys to navigate RPi on monitor (believe ctrl+t is 
        to bring up terminal which is needed here, otherwise google how to bring 
        up terminal with hotkeys)
            - vim and nano are two good terminal text editors to use here. If never 
            used before, google how to use
            - Always use `sudo` before opening files. Root user access is needed
            - Using these text editors requires special commands for saving / 
            quiting. For instance, on vim to save is ESC then `:q` then ENTER 
            and quitting is ESC then `:w` then ENTER. Look these up to avoid 
            accidentally not saving files,
        6. Continue to next main step
    - Use mini SD card reader and plug into PC
        1. NOTE: This was not the solution used by previous team but is a proposed 
        solution. Files needed may be unable to be read or encrypted. Best to use 
        a Linux machine for reading these files
        2. Once mini SD card is in computer and readable, continue below
4. Open `/etc/wpa_supplicant/wpa_supplicant.conf`
5. Create new network entry based off of previous entries. 
    - ssid = name of wifi to connect to
    - psk = password for wifi
    - id_str = unique ID string which will be used later. Make sure this is different 
    than all other id_str entries for other networks.
6. Save and quit file. 
7. Open `/etc/network/interfaces`
8. You will see a couple blocks with "iface [id_str] inet static". For each network 
you want to add, add another entry above these. The RPi will try to connect to 
these networks in the order that they are in so be sure to add highest priority first.
9. When adding new entries know...
    - Add id_str from networks added to wpa_supplicant.conf in header line
    - address = IP that RPi will be at once connected to WiFi
        - When trying to SSH in later, this is the IP you will need to connect to
        - It is best this way because IP will always be the same for RPi on this 
        network instead of sometimes switching upon reconnection.
        - NOTE: When finding IP address to input, take the IP of your computer 
        while on the hotspot (from the `ifconfig` or `ipconfig` command) and 
        set your RPi's IP to be close to your computer's IP.
            - For example if your computer's IP on the hotspot is 192.168.1.222, 
            it might be good to set your RPi's IP to 192.168.1.224.
            - This should be done based off an issue encountered with Fall 2018 
            team where one phone hotspot was switched out (iPhone changed to 
            Android) and only the gateway IP was changed. For some reason 
            when attempting to connect to the old RPi IP set up for the iPhone 
            hotspot, SSH could not be established. The IP was then reset to be 
            closer to a computer's IP when connected to the hotspot and then 
            an SSH connection could be established.
    - netmask = Typcially 255.255.255.0 see next point for how to find
    - gateway = Hotspot base address
    - FINDING NETMASK AND GATEWAY
        1. With your PC, connect to hotspot you are trying to set up on RPi. On 
        Linux open command line and type `ifconfig`. On Windows do the same 
        but type `ipconfig`.
        2. Within the result you will be able to find netmask and gateway IP 
        addresses to add into netmask and gateway fields on RPi.
10. Save file and exit
11. If mini SD card was taken out of RPi, safely eject it from your computer and 
put back into RPi.
12. Reboot RPi, and make sure Hotspot is on.
13. RPi may take a couple minutes to boot up and connect to hotspot so be patient.
    - Using phone as hotspot can help here because most phones will indicate 
    how many devices are connected. Therefore you will be able to see when 
    the RPi connects.
14. Once RPi is connected to hotspot, SSH into it at the pi user
    - With Windows you will need to download an SSH software such as putty or 
    MobaXTerm
    - With Linux simply open a command prompt and enter `ssh pi@[Previously set RPi 
    IP]`

### Control Circuit Integration
- Within the circuit to control the prosthetic hand there are 3 main components
    1. RPi Zero W
    2. PCA9685 PWM Controller
    3. Servo Motors
- These components should be hooked up in the configuration outlined in the schematic below. 
Circuit can also be found [here](docs/SystemDiagramsandImages/prostheticController.png)
- When hooking up the servos, be sure to put them in the PCA9685 PWM slots from left to right.
    1. The order the servos have been hooked up in has changed many times. It is 
    easy to change this configuration within the [motion.py](myo-arm-control/motion.py) 
    script. Within `class Motion`'s `__init__` function just reorder the class's 
    `self.motor_order` list.
    2. Alternatively, you could just figure out which figure out which function moves 
    which finger then reconfigure the connections on the PCA9685 board but this 
    is a more annoying method considering all of the wires that have to be unplugged 
    and plugged back in.
    
![Circuit Schematic](docs/SystemDiagramsandImages/prostheticController.png)

### Python Scripts
#### Dependencies
1. Python 3.5+
    - Any Python 3 version should work but everything was developed and tested with
    Python 3.5+. 
    - NOTE: Python 2 may be used for scripts in [Previous Work](/Previous Work) 
    directory but not all scripts in this directory were tested or run.

#### Before first run...
1. Open powershell in raw-myo-plot directory
2. Run command...
```
python3 config.py
```
3. Enter path to MYO SDK bin folder
    1. Example: C:\Users\ROWAN\Documents\prostheticClinic\myo-sdk-win-0.9.0\bin
4. Direct powershell to repository root directory and run...

`pip3 install -r requirements.txt`

    - If any missing library issues come up while running Python scripts, please
    add them to the requirements.txt file once correct package is found and installed.

Troubleshooting Known Errors
----------------------------
### Running raw_myo_plot.py: When connection to MYO hub cannot be created.
- Usually happens when hub is not shut down before script is shut down.
    - TO FREE MYO HUB:
        1. Open task manager, close MYO Connect program or service
        2. Re-open MYO Connect
        3. Retry running script
        4. If same error occurs, connect MYO to computer via USB for a minute
        5. Disconnect MYO, put back on arm
        6. Retry running script
        7. If error still persists, restart computer.
        
### Running raw_myo_plot.py: When WinError 126 is thrown from loading SDK_BIN_PATH
- Usually happens when SDK path within myo.config file is incorrect
    - TO CORRECT THIS PATH:
        1. Find where MYO SDK is. It should be in repo root under 
        myo-sdk-win-0.9.0\bin.
        2. Delete raw-myo-plot\myo.config
        3. Follow steps 2 and 3 from [before first run setup](#before-first-run...)
        4. Retry running raw_myo_ploy.py