# Prosthetic Arm Engineering Clinic
#### Rowan University
#### Department of Electrical and Computer Engineering
#### Advisor: Dr. Rasool
#### First Commit - Fall Semester 2018

SETUP
-----

#### Dependencies
1. Python 3.5+

#### Before first run...
1. Open powershell in raw-myo-plot directory
2. Run command...
```
python3 config.py
```
3. Enter path to MYO SDK bin folder
    1. Example: C:\Users\ROWAN\Documents\prostheticClinic\myo-sdk-win-0.9.0\bin
4. Direct powershell to repository root directory and run...
```
pip3 install -r requirements.txt
```

Troubleshooting Known Errors
----------------------------
### When connection to MYO hub cannot be created.
    - Usually happens when hub is not shut down before script is shut down.
    - TO FREE MYO HUB:
        1. Open task manager, close MYO Connect program or service
        2. Re-open MYO Connect
        3. Retry running script
        4. If same error occurs, connect MYO to computer via USB for a minute
        5. Unconnect MYO, put back on arm
        6. Retry running script
        7. If error still persists, restart computer.