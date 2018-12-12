# Previous Work from Fall 2017 and Spring 2018 Team
### Documentation created by Fall 2018 team for ease of use by future teams

### This is a recording / outline of all files reviewed by documenting team

Important Files and Folders
---------------------------
1. Most important: folder rpi_code
    - This is an outdated version of the code found on the raspberry pi. If any files 
    within this directory are not within new code or documents, it has not been touched. 
    - Further documentation on files contained within this folder can be found in same 
    directory as respective files.
2. Algorithms
    - Good starting point for creating machine learning algorithms

All Files
---------
## Folders
1. Data
    - Includes CSV files of data recordings from previous team. Cannot tell exactly 
    what data is recorded but it is assumed to be EMG channels 1 - 8 for a 
    rest position.
2. Data2
    - Seems to be more files of the same type as found in Data folder
3. Data3Combo
    - Seems to be more files of the same type as found in Data folder
4. Data4
    - Includes CSV files of data recordings for open hand then closed hand gestures. 
    Data is 8-channel reading of EMG signals.
5. Pickled_data, pickled_data2, pickled_data3combo
    - Includes pkl files of CSVs in respective CSV folders. Unknown why previous
    team pickled their data but can be decoded with python.
6. rpi_code
    - Code found on raspberry pi zero at `~/share/Myo4Linux`
    - NOTE: Code on RPi should be considered to be most up to date version
7. testForceSensor, testSerialRead, testServo
    - DEPRECIATED: Arduino code files but Arduino was replaced by Raspberry Pi Zero 
    by last team.
    
## Files
1. Algorithms.py
    - Python File
    - Python module for creating different machine learning algorithms. Only LDA 
    class was complete.
2. ChrisAngelini_test1.pickle, *_test2.pickle and *_test3.pickle
    - Pickle Files
    - Record files, can be decoded by Python, unknown gesture or contained data
3. data.csv, data3.csv
    - Comma Separated Value Files
    - Record files of EMG data in rest gesture
4. dataBin.pickle
    - Pickle File
    - Unknown what this file is contained but can be decoded with Python
5. DataBin.py
    - Python File
    - Reads in CSV and formats MyoBand data in proper data bins
6. DataIO.py
    - Python File
    - Module for handling recorded data, can read CSV and pickle files. Also 
    can convert CSVs to pickle files.
7. DataPreprocessing.py
    - Python File
    - Module for preprocessing data received from MYO band before sending to arm
8. FeatureExtraction.py
    - Python File
    - Module for extracting features from record files
9. runMyoPose.py
    - Python File
    - DEPRECIATED: Python file for interacting with Arduino to run selected poses 
    on arm
10. Test_Preprocessing.py
    - Python File
    - Test module for DataPreprocessing module
11. testAng*_LDA.pickle
    - Pickle Files
    - Record files for MYO data captured but unknown poses
12. testArmCNN.py
    - Python File
    - Data preprocessing and cleaning before creating LSTM and feeding data into that
13. All .h5 files
    - h5 files
    - Records that can be loaded to load in trained artificial neural network models
14. testExtractFeatures.py, testLDA.py, testMyoEMGStream.py, testMyoStream.py, 
testScript.py, testScript2.py, testStreamLSTM.py
    - Python Files
    - Test files for data capturing, preprocessing and classification by LSTM network
15. testSerialWrite.py
    - Python File
    - DEPRECIATED: For writing to Arduino
16. trainAlgorithms.py
    - Python File
    - Used for training machine learning algorithms off of recorded data.