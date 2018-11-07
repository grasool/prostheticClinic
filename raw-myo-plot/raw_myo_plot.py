from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg 

import data_collector, os
import myo as libmyo #; libmyo.init()
from myo_listener import Listener

import numpy as np

import sys, time

EMG_RANGE = 8
ORI_RANGE = 4
ACC_RANGE = 3

#class RawWindow(QtGui.QWidget):
class RawWindow(QtGui.QMainWindow):
    def __init__(self):
        # Sets up window
        super(RawWindow, self).__init__()
        
        # Sets main window bar title and size
        self.setWindowTitle('Myo Data Acquirer')
        self.resize(800,480)
        
        # Sets refresh rate for plots and default record time
        self.record_time = 0.5
        self.toggle_snipping = True
        self.sample_rate = 200 # Hz - 200 default for MYO Band
        self.refreshRate = 1/self.sample_rate
        
        # Bool for first run so program knows to show window
        self.firstWin = True
        self.settings_open = False
        
        self.all_plots()
        
    def revert_to_all_plots(self):
        # Closes last window then goes back to main screen
        self.cw.close()
        self.all_plots()
        
    def all_plots(self):
        """
            Screen: all_plots
            Desc: Shows EMG, acceleration and orientation plots for raw
                MYO inputs. All channels for like-fields are shown on same
                plot (8 channels for EMG, 3 channels for acceleration and
                4 channels for orientation).
        """
        # Creates QtGUI widget and sets layout
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        l = QtGui.QGridLayout()
        self.cw.setLayout(l)
        
        # Creates inner widget label for screen title
        titleLabel = QtGui.QLabel('Myo Data Acquirer')
        titleLabel.setFont(QtGui.QFont("Garamond", 16, QtGui.QFont.Bold))
        l.addWidget(titleLabel, 0, 0, 2, 1)
        
        # Creates button to go to EMG plots screen
        emg_button = QtGui.QPushButton('EMG Plots')
        emg_button.setToolTip('Open only EMG plots.')
        emg_button.clicked.connect(self.emg_plots)
        l.addWidget(emg_button, 0, 0, 1, 1)
        
        # Shows EMG plot
        self.emgplot = pg.PlotWidget(name='EMGplot')
        self.emgplot.setRange(xRange=(0, 1000), yRange=(-50, 400))#QtCore.QRectF(-50,-200,1000,1400))
        self.emgplot.disableAutoRange()
        self.emgplot.setTitle("EMG")
        l.addWidget(self.emgplot, 0, 1, 1, 1)

        # Shows acceleration plot
        self.accplot = pg.PlotWidget(name='ACCplot')
        self.accplot.setRange(QtCore.QRectF(0,-2,1000,7))
        self.accplot.setTitle("Accelerometer")
        l.addWidget(self.accplot, 1, 1, 1, 1)
        
        # Creates button to go to acceleration plots screen
        acc_button = QtGui.QPushButton('Acceleration Plots')
        acc_button.setToolTip('Open only acceleration plots.')
        acc_button.clicked.connect(self.acc_plots)
        l.addWidget(acc_button, 1, 0, 1, 1)

        # Shows orientation plot
        self.oriplot = pg.PlotWidget(name='ORIplot')
        self.oriplot.setRange(QtCore.QRectF(0,-1,1000,8))
        self.oriplot.setTitle("Orientation")
        l.addWidget(self.oriplot, 2, 1, 1, 1)
        
        # Creates button to go to orientation plots screen
        ori_button = QtGui.QPushButton('Orientation Plots')
        ori_button.setToolTip('Open only orientation plots.')
        ori_button.clicked.connect(self.ori_plots)
        l.addWidget(ori_button, 2, 0, 1, 1)
        
        # Creates list for EMG recordings then starts recording buffer
        # readings. Plots EMG buffer data on plot as well.
        self.emgcurve = []
        for i in range(8):
            c = self.emgplot.plot(pen=(i,10))
            c.setPos(0,i*50)
            self.emgcurve.append(c)
        
        # Creates list for acceleration recordings then starts recording buffer
        # readings. Plots acceleration buffer data on plot as well.
        self.oricurve = []
        for i in range(4):
            c = self.oriplot.plot(pen=(i,5))
            c.setPos(0,i*2)
            self.oricurve.append(c)

        # Creates list for orientation recordings then starts recording buffer
        # readings. Plots acceleration buffer data on plot as well.
        self.acccurve = []
        for i in range(4):
            c = self.accplot.plot(pen=(i,5))
            c.setPos(0,i*2)
            self.acccurve.append(c)
        
        # Gets current time so system knows when plots were updated
        self.lastUpdateTime = time.time()
        
        # Sets variable for selective plot updating
        self.window_type = 'all'
        
        # If first run, show plots
        if self.firstWin:
            self.show()
            self.start_listening()
            self.firstWin = False
    
    def emg_plots(self):
        """
            Screen: emg_plots
            Desc: Shows each EMG channel from MYO device on separate 
                plot. Also allows for recording of EMG, acc and ori
                data.
        """
        # Closes previous widget in main window
        self.cw.close()
        
        # Creates new widget and sets layout for EMG plots
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        self.l = QtGui.QGridLayout()
        self.cw.setLayout(self.l)
        
        # Sets up widget label title
        titleLabel = QtGui.QLabel('Myo Data Acquirer')
        titleLabel.setFont(QtGui.QFont("Garamond", 16, QtGui.QFont.Bold))
        self.l.addWidget(titleLabel, 0, 0, 2, 1)
        
        # Creates button to go back to all plots main screen
        all_button = QtGui.QPushButton('All Plots')
        all_button.setToolTip('Open all plots.')
        all_button.clicked.connect(self.revert_to_all_plots)
        self.l.addWidget(all_button, 0, 0, 1, 1)
        
        # Creates button to start recording data to output as CSV
        record = QtGui.QPushButton('Record Data')
        record.setToolTip('Record MYO Data')
        record.setStyleSheet("background-color: green")
        record.clicked.connect(self.toggle_record)
        self.record = record
        self.l.addWidget(record, 1, 0, 1, 1)
        
        save_plot_data = QtGui.QPushButton('Save Plotted Data')
        save_plot_data.setToolTip('Save MYO data seen on plots')
        save_plot_data.setStyleSheet('background-color: green')
        save_plot_data.clicked.connect(self.record_plot_data)
        self.save_plot_data = save_plot_data
        self.l.addWidget(save_plot_data, 2, 0, 1, 1)
        
        # Creates empty list for each EMG channel to be put on seperate plots
        self.emgplot_channels = []
        j = 0 # Subplot positioning variable
        for i in range(EMG_RANGE):
            # If 4 rows have already been filled with plots, move to next column
            if i == 4:
                j = 1
                
            # Sets up plot widget for single channel and appends to channels list
            self.emgplot_channels.append(pg.PlotWidget(name='EMG Channel %s' % (i+1)))
            
            # Sets up range and plot title
            self.emgplot_channels[-1].setRange(xRange=(0, 1000), yRange=(-50, 50))
            self.emgplot_channels[-1].disableAutoRange()
            self.emgplot_channels[-1].setTitle("EMG Channel %s" % (i+1))
            
            # Adds plot to widget in specific position
            self.l.addWidget(self.emgplot_channels[-1], i-(j*4), 1+j, 1, 1)
        
        # Sets up EMG curves and plots on separate plots
        self.emgcurve = []
        for i in range(8):
            c = self.emgplot_channels[i].plot(pen=(i,10))
            c.setPos(0,0)
            self.emgcurve.append(c)
            
        # Creates button to go back to all plots main screen
        record_config = QtGui.QPushButton('Record Configuration')
        record_config.setToolTip('Configure recording options.')
        record_config.clicked.connect(self.record_settings)
        self.l.addWidget(record_config, 4, 0, 1, 1)
        #self.record_settings()
        
        self.settingsTick = QtGui.QLabel(self.get_settings_tick())
        self.settingsTick.setFont(QtGui.QFont("Garamond", 10, QtGui.QFont.Bold))
        self.l.addWidget(self.settingsTick, 4, 1, 1, 1)
        
        self.lastUpdateTime = time.time()
        
        # Sets variable for selective plot updating
        self.window_type = 'emg'
      
    def acc_plots(self):
        """
            Screen: acc_plots
            Desc: Shows each channel for MYO acceleration readings on separate
            plots. Also allows for recording of all MYO data.
        """
        # Closes previous plot widget in main window
        self.cw.close()
        
        # Creates new plot widget and layout and puts in main window
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        self.l = QtGui.QGridLayout()
        self.cw.setLayout(self.l)
        
        # Creates widget title label
        titleLabel = QtGui.QLabel('Acceleration Plots')
        titleLabel.setFont(QtGui.QFont("Garamond", 16, QtGui.QFont.Bold))
        self.l.addWidget(titleLabel, 0, 0, 2, 1)
        
        # Creates button to go back to all plots main screen
        all_button = QtGui.QPushButton('All Plots')
        all_button.setToolTip('Open all plots.')
        all_button.clicked.connect(self.revert_to_all_plots)
        self.l.addWidget(all_button, 0, 0, 1, 1)
        
        # Creates button for recording all MYO data
        record = QtGui.QPushButton('Record Data')
        record.setToolTip('Record MYO Data')
        record.setStyleSheet("background-color: green")
        record.clicked.connect(self.toggle_record)
        self.record = record
        self.l.addWidget(record, 1, 0, 1, 1)
        
        save_plot_data = QtGui.QPushButton('Save Plotted Data')
        save_plot_data.setToolTip('Save MYO data seen on plots')
        save_plot_data.setStyleSheet('background-color: green')
        save_plot_data.clicked.connect(self.record_plot_data)
        self.save_plot_data = save_plot_data
        self.l.addWidget(save_plot_data, 2, 0, 1, 1)
        
        # Creates list to be filled with acc channel plots
        self.accplot_channels = []
        self.acccurve= []
        for i in range(ACC_RANGE):
            # Creates plot widget
            self.accplot_channels.append(pg.PlotWidget(name='Acceleration Channel %s' % (i+1)))
            
            # Sets range and channel plot title
            self.accplot_channels[-1].setRange(QtCore.QRectF(0,-2,1000,7))
            self.accplot_channels[-1].disableAutoRange()
            self.accplot_channels[-1].setTitle("Acceleration Channel %s" % (i+1))
            
            # Adds plot to screen widget
            self.l.addWidget(self.accplot_channels[-1], i, 1, 1, 1)
            
            # Gets acc buffer data and puts on plot
            c = self.accplot_channels[i].plot(pen=(i,10))
            c.setPos(0,0)
            self.acccurve.append(c)
            
        # Creates button to go back to all plots main screen
        record_config = QtGui.QPushButton('Record Configuration')
        record_config.setToolTip('Configure recording options.')
        record_config.clicked.connect(self.record_settings)
        self.l.addWidget(record_config, 4, 0, 1, 1)
        #self.record_settings()
        
        self.settingsTick = QtGui.QLabel(self.get_settings_tick())
        self.settingsTick.setFont(QtGui.QFont("Garamond", 10, QtGui.QFont.Bold))
        self.l.addWidget(self.settingsTick, 4, 1, 2, 1)
        
        # Gets time acc plots were updated
        self.lastUpdateTime = time.time()
        
        # Sets variable for selective plot updating
        self.window_type = 'acc'
    
    def ori_plots(self):
        """
            Screen: ori_plots
            Desc: Shows each channel for MYO orientation data on separate 
                plots. Also allows for recording of data.
        """
        # Closes previous plot widget
        self.cw.close()
        
        # Creates new plot widget and sets layout for orientation plots
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        self.l = QtGui.QGridLayout()
        self.cw.setLayout(self.l)
        
        # Creates plot widget title label
        titleLabel = QtGui.QLabel('Orientation Plots')
        titleLabel.setFont(QtGui.QFont("Garamond", 16, QtGui.QFont.Bold))
        self.l.addWidget(titleLabel, 0, 0, 2, 1)
        
        # Creates button to go back to all plots main screen
        all_button = QtGui.QPushButton('All Plots')
        all_button.setToolTip('Open all plots.')
        all_button.clicked.connect(self.revert_to_all_plots)
        self.l.addWidget(all_button, 0, 0, 1, 1)
        
        # Creates button to start recording data
        record = QtGui.QPushButton('Record Data')
        record.setToolTip('Record MYO Data')
        record.setStyleSheet("background-color: green")
        record.clicked.connect(self.toggle_record)
        self.record = record
        self.l.addWidget(record, 1, 0, 1, 1)
        
        save_plot_data = QtGui.QPushButton('Save Plotted Data')
        save_plot_data.setToolTip('Save MYO data seen on plots')
        save_plot_data.setStyleSheet('background-color: green')
        save_plot_data.clicked.connect(self.record_plot_data)
        self.save_plot_data = save_plot_data
        self.l.addWidget(save_plot_data, 2, 0, 1, 1)
        
        # Creates list for orientation channel plots
        self.oriplot_channels = []
        self.oricurve = []
        for i in range(ORI_RANGE):
            # Creates plot widget
            self.oriplot_channels.append(pg.PlotWidget(name='Orientation Channel %s' % (i+1)))
            
            # Sets range and title for plot
            self.oriplot_channels[-1].setRange(QtCore.QRectF(0,-1,1000,8))
            self.oriplot_channels[-1].disableAutoRange()
            self.oriplot_channels[-1].setTitle("Orientation Channel %s" % (i+1))
            
            # Adds widget to screen
            self.l.addWidget(self.oriplot_channels[-1], i, 1, 1, 1)
            
            # Gets orientation buffer data and puts on plot
            c = self.oriplot_channels[i].plot(pen=(i,10))
            c.setPos(0,0)
            self.oricurve.append(c)
            
        # Creates button to go back to all plots main screen
        record_config = QtGui.QPushButton('Record Configuration')
        record_config.setToolTip('Configure recording options.')
        record_config.clicked.connect(self.record_settings)
        self.l.addWidget(record_config, 4, 0, 1, 1)
        #self.record_settings()
        
        self.settingsTick = QtGui.QLabel(self.get_settings_tick())
        self.settingsTick.setFont(QtGui.QFont("Garamond", 10, QtGui.QFont.Bold))
        self.l.addWidget(self.settingsTick, 4, 1, 2, 1)
        
        self.lastUpdateTime = time.time()
        
        # Sets data update variable
        self.window_type = 'ori'
        
    def record_settings(self):
        if not self.settings_open:
            self.r = RecordSettings(self)
            self.r.show()
            self.settings_open = True
            
    def save_settings(self):
        try:
            self.sample_rate = float(self.r.samplerate.text())
            self.refreshRate = 1/self.sample_rate
            self.record_time = float(self.r.numentry.text())
            self.settingsTick.setText(self.get_settings_tick())
        except ValueError as e1:
            QMessageBox.about(self, "ERROR", "Settings could not be saved. Input value is invalid float value.")
        
    def get_settings_tick(self):
        out = "Sample Rate: %s Hz | " % (self.sample_rate)
        out += "Record Time: %s s | " % (self.record_time)
        out += "Snipping Window: %s" % ("ON" if self.toggle_snipping else "OFF")
        
        return out
        
    def toggle_snipping_window(self, state):
        print(self.toggle_snipping)
        self.toggle_snipping = state
        
    def toggle_record(self):
        # Toggles data recording if button is pressed
        
        if self.record_time > 0:
            self.myo_data_record.timed_record(self.sample_rate, self.record_time)
            
        # If data was just being recorded...
        if self.myo_data_record.recording:
            # Save recorded data stream and output filename
            # NOTE: Record buffer is also reset within this function
            filename = self.myo_data_record.save_record()
            print('Record saved at %s' % filename)
            
            # Reset record data button back to green and original label
            self.record.setStyleSheet("background-color: green")
            self.record.setText("Record Data")
            self.record.setToolTip('Record MYO Data')

        else: # If data is to start being recorded...
            # Set record data button to red and change label
            self.record.setStyleSheet("background-color: red")
            self.record.setText("Stop Recording")
            self.record.setToolTip('Stop Recording MYO Data')
            
        # Toggle recording bool on data recording instance
        # NOTE: Any time recording is True, record buffer will be updated
            # when plots are updated.
        self.myo_data_record.toggle_recording()
        
    def record_plot_data(self):
        filename = self.myo_data_record.save_plot_data(self.listener)
        
        print('Plot record saved at %s' % filename)
        
    def start_listening(self):
        # Starts listenening to MYO device
        self.myo_data_record = data_collector.myo_data_collector()
        self.listener = Listener(self)
        try:
            self.hub = libmyo.Hub()
            self.hub.set_locking_policy(libmyo.LockingPolicy.none)
            self.hub.run(1000, self.listener)
        except:
            print('\n\nNo Myo found... Showing plot for dev purposes...')

    def update_plots(self):
        # Gets current time
        ctime = time.time()
        
        # Gets window being displayed - doing this for shorter logic later
        win = self.window_type
        
        # If time to refresh has been passed, update data
        if (ctime - self.lastUpdateTime) >= self.refreshRate:
            # Resets update time
            self.lastUpdateTime = ctime
            
            # If recording is true, record buffer will be updated
            self.myo_data_record.collect(self.listener, ctime)
            
            if self.myo_data_record.samples_left > 0:
                self.record.setText((str((self.myo_data_record.samples_left/
                                        (self.sample_rate*self.record_time))*
                                        self.record_time)+'   ')[:4])
            elif int(self.myo_data_record.samples_left) == 0:
                self.toggle_record()
                
            if win == 'all' or win == 'emg': # Updates EMG data
                for i in range(EMG_RANGE):
                    try:
                        # Try-except fixes error that sometimes occurs where
                            # emgcurve list is not initialized to correct
                            # size. Do now know why error occurs but this is
                            # a fix until origin can be found and patched.
                        self.emgcurve[i].setData(self.listener.emg.data[i,:])
                    except IndexError as e1:
                        print('EMG index not initialized correctly... Fixing...')
            if win == 'all' or win == 'ori': # Updates ori data
                for i in range(ORI_RANGE):
                    try:
                        self.oricurve[i].setData(self.listener.orientation.data[i,:])
                    except IndexError as e2:
                        print('ORI index not initialized correctly... Fixing...')
            if win == 'all' or win == 'acc': # Updates acc data
                for i in range(ACC_RANGE):
                    try:
                        self.acccurve[i].setData(self.listener.acc.data[i,:])
                    except IndexError as e3:
                        print('ACC index not initialized correctly... Fixing...')
                        
            app.processEvents() # Tells plots to update with new data
        
    def closeEvent(self, event, restart=0):
        # Shuts down MYO connection.
        # NOTE: THIS MUST BE DONE OR MYO MAY BECOME LOCKED AND IT IS ANNOYING
            # TO UNLOCK. Check README for how to unlock
        print("Closing...")
        self.hub.shutdown()
        
# Class for record configuration window pop up
class RecordSettings(QtGui.QMainWindow):
    def __init__(self, parent=None, rownum=0):
        global window
        
        # Sets up window
        super(RecordSettings, self).__init__(parent)
        
        # Sets main window bar title and size
        self.setWindowTitle('Myo Data Recorder Settings')
        self.resize(400,240)
        
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        self.l = QtGui.QGridLayout()
        self.cw.setLayout(self.l)
        
        seconds = QtGui.QLabel('Seconds\n(Set to 0 for manual toggling)')
        self.l.addWidget(seconds, 0, 0, 1, 1)
        
        self.numentry = QtGui.QLineEdit()
        self.numentry.setText(str(window.record_time))
        self.l.addWidget(self.numentry, 0, 1, 1, 1)
        
        seconds = QtGui.QLabel('Device Sample Rate (Hz)')
        self.l.addWidget(seconds, 1, 0, 1, 1)
        
        self.samplerate = QtGui.QLineEdit()
        self.samplerate.setText(str(window.sample_rate))
        self.l.addWidget(self.samplerate, 1, 1, 1, 1)
        
        snipping_toggle = QtGui.QCheckBox('Toggle Snipping Window')
        snipping_toggle.setChecked(window.toggle_snipping)
        snipping_toggle.toggled.connect(window.toggle_snipping_window)
        self.l.addWidget(snipping_toggle, 2, 1, 1, 1)
        
        save_plot_data = QtGui.QPushButton('Save')
        save_plot_data.setToolTip('Save MYO Settings')
        save_plot_data.clicked.connect(window.save_settings)
        self.save_plot_data = save_plot_data
        self.l.addWidget(save_plot_data, 3, 0, 1, 1)
        
        save_plot_data = QtGui.QPushButton('Exit')
        save_plot_data.clicked.connect(self.close)
        self.l.addWidget(save_plot_data, 3, 1, 1, 1)
        
    def closeEvent(self, event=0, restart=0):
        global window
        
        window.settings_open = False
        
class SnippingWindow(QtGui.QMainWindow):
    def __init__(self, filename):
        # Sets up window
        super(RawWindow, self).__init__()

        # Sets main window bar title and size
        self.setWindowTitle('Record Snipper')
        self.resize(800,480)
        
        self.load_record(filename)
        self.all_plots()
        
    def load_record(self, filename):
        df = pd.read_csv(filename)
        self.emg = np.array([[]]*EMG_RANGE)
        self.acc = np.array([[]]*ACC_RANGE)
        self.ori = np.array([[]]*ORI_RANGE)
        
        for col in list(df):
            try: # Should only fail on time column
                num = int(col.split('_')[-1])
            except:
                pass
                
            if 'emg' in col.lower():
                self.emg[num] = df[col].tolist()
            elif 'acc' in col.lower():
                self.acc[num] = df[col].tolist()
            elif 'ori' in col.lower():
                self.ori[num] = df[col].tolist()
        
    def all_plots(self):
        """
            Screen: all_plots
            Desc: Shows EMG, acceleration and orientation plots for raw
                MYO inputs. All channels for like-fields are shown on same
                plot (8 channels for EMG, 3 channels for acceleration and
                4 channels for orientation).
        """
        # Creates QtGUI widget and sets layout
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        l = QtGui.QGridLayout()
        self.cw.setLayout(l)
        
        # Creates inner widget label for screen title
        titleLabel = QtGui.QLabel('Myo Data Acquirer')
        titleLabel.setFont(QtGui.QFont("Garamond", 16, QtGui.QFont.Bold))
        l.addWidget(titleLabel, 0, 0, 2, 1)
        
        # Creates button to go to EMG plots screen
        emg_button = QtGui.QPushButton('EMG Plots')
        emg_button.setToolTip('Open only EMG plots.')
        emg_button.clicked.connect(self.emg_plots)
        l.addWidget(emg_button, 0, 0, 1, 1)
        
        # Shows EMG plot
        self.emgplot = pg.PlotWidget(name='EMGplot')
        self.emgplot.setRange(xRange=(0, 1000), yRange=(-50, 400))#QtCore.QRectF(-50,-200,1000,1400))
        self.emgplot.disableAutoRange()
        self.emgplot.setTitle("EMG")
        l.addWidget(self.emgplot, 0, 1, 1, 1)

        # Shows acceleration plot
        self.accplot = pg.PlotWidget(name='ACCplot')
        self.accplot.setRange(QtCore.QRectF(0,-2,1000,7))
        self.accplot.setTitle("Accelerometer")
        l.addWidget(self.accplot, 1, 1, 1, 1)
        
        # Creates button to go to acceleration plots screen
        acc_button = QtGui.QPushButton('Acceleration Plots')
        acc_button.setToolTip('Open only acceleration plots.')
        acc_button.clicked.connect(self.acc_plots)
        l.addWidget(acc_button, 1, 0, 1, 1)

        # Shows orientation plot
        self.oriplot = pg.PlotWidget(name='ORIplot')
        self.oriplot.setRange(QtCore.QRectF(0,-1,1000,8))
        self.oriplot.setTitle("Orientation")
        l.addWidget(self.oriplot, 2, 1, 1, 1)
        
        # Creates button to go to orientation plots screen
        ori_button = QtGui.QPushButton('Orientation Plots')
        ori_button.setToolTip('Open only orientation plots.')
        ori_button.clicked.connect(self.ori_plots)
        l.addWidget(ori_button, 2, 0, 1, 1)
        
        # Creates list for EMG recordings then starts recording buffer
        # readings. Plots EMG buffer data on plot as well.
        self.emgcurve = []
        for i in range(8):
            c = self.emgplot.plot(pen=(i,10))
            c.setPos(0,i*50)
            self.emgcurve.append(c)
        
        # Creates list for acceleration recordings then starts recording buffer
        # readings. Plots acceleration buffer data on plot as well.
        self.oricurve = []
        for i in range(4):
            c = self.oriplot.plot(pen=(i,5))
            c.setPos(0,i*2)
            self.oricurve.append(c)

        # Creates list for orientation recordings then starts recording buffer
        # readings. Plots acceleration buffer data on plot as well.
        self.acccurve = []
        for i in range(4):
            c = self.accplot.plot(pen=(i,5))
            c.setPos(0,i*2)
            self.acccurve.append(c)
        
        # Gets current time so system knows when plots were updated
        self.lastUpdateTime = time.time()
        
        # Sets variable for selective plot updating
        self.window_type = 'all'
        
        # If first run, show plots
        if self.firstWin:
            self.show()
            self.start_listening()
            self.firstWin = False

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = RawWindow()
    sys.exit(app.exec_())
