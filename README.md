# Prosthetic Arm Engineering Clinic
#### Rowan University
#### Department of Electrical and Computer Engineering
#### Advisor: Dr. Rasool
#### First Commit - Fall Semester 2018 (But includes work from previous semesters never recorded on Git)

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
        5. Disconnect MYO, put back on arm
        6. Retry running script
        7. If error still persists, restart computer.
        
### When WinError 126 is thrown from loading SDK_BIN_PATH
- Usually happens when SDK path within myo.config file is incorrect
    - TO CORRECT THIS PATH:
        1. Find where MYO SDK is. It should be in repo root under 
        myo-sdk-win-0.9.0\bin.
        2. Delete raw-myo-plot\myo.config
        3. Follow steps 2 and 3 from [before first run setup](#before-first-run...)
        4. Retry running raw_myo_ploy.py