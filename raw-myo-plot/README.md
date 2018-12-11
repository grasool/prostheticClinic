# raw-myo-plot
Raw Myo Plot grabs the raw data streams from a Thalmic Myo and displays them in real-time.

Myo data is acquired using [myo-python](https://github.com/NiklasRosenstein/myo-python).

All Files
---------
1. config.py
    - Module for creating config files. Config files will not be uploaded to GitHub 
    and should be unique to each computer. 
    - Config Fields
        - sdk_path: User's path to the myo-sdk-win-0.9.0 bin folder
        - save_scheme: Scheme to use when outputting recorded data
2. data_collector.py
    - Module for collecting and saving data
3. Extract_Features.py
    - Module for extracting features from records
4. myo_listener.py
    - Module for getting data from MYO band
5. plotpicker.py
    - Module for picking record and plotting it
6. raw_myo_plot.py
    - Module for plotting and interacting with MYO data. Run using `python3 raw_myo_plot
    .py -s` to bring up record snipping GUI.
    - Save schemes can also be edited within MYO plotter. 
    - Can either record live data as it comes in or record data currently plotted.
    - Record snipper will output files with original filenames and '_snipped' appended.