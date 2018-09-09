"""
RawMyo.py

jdaly
5/20/2015

Raw Myo data acquisition and display
"""

from pyqtgraph.Qt import QtGui, QtCore
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
        super(RawWindow, self).__init__()
        
        self.setWindowTitle('Myo Data Acquirer')
        self.resize(800,480)
        self.firstWin = True
        
        self.all_plots()
        
    def revert_to_all_plots(self):
        self.cw.close()
        self.all_plots()
        
    def all_plots(self):
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        l = QtGui.QGridLayout()
        self.cw.setLayout(l)
        
        titleLabel = QtGui.QLabel('Myo Data Acquirer')
        titleLabel.setFont(QtGui.QFont("Garamond", 16, QtGui.QFont.Bold))
        l.addWidget(titleLabel, 0, 0, 2, 1)
        
        emg_button = QtGui.QPushButton('EMG Plots')
        emg_button.setToolTip('Open only EMG plots.')
        emg_button.clicked.connect(self.emg_plots)
        l.addWidget(emg_button, 0, 0, 1, 1)
        
        self.emgplot = pg.PlotWidget(name='EMGplot')
        self.emgplot.setRange(xRange=(0, 1000), yRange=(-50, 400))#QtCore.QRectF(-50,-200,1000,1400))
        self.emgplot.disableAutoRange()
        self.emgplot.setTitle("EMG")
        l.addWidget(self.emgplot, 0, 1, 1, 2)

        self.accplot = pg.PlotWidget(name='ACCplot')
        self.accplot.setRange(QtCore.QRectF(0,-2,1000,7))
        self.accplot.setTitle("Accelerometer")
        l.addWidget(self.accplot, 1, 1, 1, 2)
        
        acc_button = QtGui.QPushButton('Acceleration Plots')
        acc_button.setToolTip('Open only acceleration plots.')
        acc_button.clicked.connect(self.acc_plots)
        l.addWidget(acc_button, 1, 0, 1, 1)

        self.oriplot = pg.PlotWidget(name='ORIplot')
        self.oriplot.setRange(QtCore.QRectF(0,-1,1000,8))
        self.oriplot.setTitle("Orientation")
        l.addWidget(self.oriplot, 2, 1, 1, 2)
        
        ori_button = QtGui.QPushButton('Orientation Plots')
        ori_button.setToolTip('Open only orientation plots.')
        ori_button.clicked.connect(self.ori_plots)
        l.addWidget(ori_button, 2, 0, 1, 1)

        self.refreshRate = 0.05
        
        self.emgcurve = []
        for i in range(8):
            c = self.emgplot.plot(pen=(i,10))
            c.setPos(0,i*50)
            self.emgcurve.append(c)

        self.oricurve = []
        for i in range(4):
            c = self.oriplot.plot(pen=(i,5))
            c.setPos(0,i*2)
            self.oricurve.append(c)

        self.acccurve = []
        for i in range(4):
            c = self.accplot.plot(pen=(i,5))
            c.setPos(0,i*2)
            self.acccurve.append(c)
        
        self.lastUpdateTime = time.time()
        
        self.window_type = 'all'
        
        if self.firstWin:
            self.show()
            self.start_listening()
            self.firstWin = False
    
    def emg_plots(self):
        self.cw.close()
        
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        self.l = QtGui.QGridLayout()
        self.cw.setLayout(self.l)
        
        titleLabel = QtGui.QLabel('Myo Data Acquirer')
        titleLabel.setFont(QtGui.QFont("Garamond", 16, QtGui.QFont.Bold))
        self.l.addWidget(titleLabel, 0, 0, 2, 1)
        
        emg_button = QtGui.QPushButton('All Plots')
        emg_button.setToolTip('Open all plots.')
        emg_button.clicked.connect(self.revert_to_all_plots)
        self.l.addWidget(emg_button, 0, 0, 1, 1)
        
        record = QtGui.QPushButton('Record Data')
        record.setToolTip('Record MYO Data')
        record.setStyleSheet("background-color: green")
        record.clicked.connect(self.toggle_record)
        self.record = record
        self.l.addWidget(record, 1, 0, 1, 1)
        
        self.emgplot_channels = []
        j = 0
        for i in range(EMG_RANGE):
            if i == 4:
                j = 1
                
            self.emgplot_channels.append(pg.PlotWidget(name='EMG Channel %s' % (i+1)))
            self.emgplot_channels[-1].setRange(xRange=(0, 1000), yRange=(-50, 50))
            self.emgplot_channels[-1].disableAutoRange()
            self.emgplot_channels[-1].setTitle("EMG Channel %s" % (i+1))
            self.l.addWidget(self.emgplot_channels[-1], i-(j*4), 1+j, 1, 1)

        self.refreshRate = 0.05
        
        self.emgcurve = []
        for i in range(8):
            c = self.emgplot_channels[i].plot(pen=(i,10))
            c.setPos(0,0)
            self.emgcurve.append(c)
        
        self.lastUpdateTime = time.time()
        
        self.window_type = 'emg'
      
    def acc_plots(self):
        self.cw.close()
        
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        self.l = QtGui.QGridLayout()
        self.cw.setLayout(self.l)
        
        titleLabel = QtGui.QLabel('Myo Data Acquirer')
        titleLabel.setFont(QtGui.QFont("Garamond", 16, QtGui.QFont.Bold))
        self.l.addWidget(titleLabel, 0, 0, 2, 1)
        
        emg_button = QtGui.QPushButton('All Plots')
        emg_button.setToolTip('Open all plots.')
        emg_button.clicked.connect(self.revert_to_all_plots)
        self.l.addWidget(emg_button, 0, 0, 1, 1)
        
        record = QtGui.QPushButton('Record Data')
        record.setToolTip('Record MYO Data')
        record.setStyleSheet("background-color: green")
        record.clicked.connect(self.toggle_record)
        self.record = record
        self.l.addWidget(record, 1, 0, 1, 1)
        
        self.accplot_channels = []
        for i in range(ACC_RANGE):
                
            self.accplot_channels.append(pg.PlotWidget(name='Acceleration Channel %s' % (i+1)))
            self.accplot_channels[-1].setRange(QtCore.QRectF(0,-2,1000,7))
            self.accplot_channels[-1].disableAutoRange()
            self.accplot_channels[-1].setTitle("Acceleration Channel %s" % (i+1))
            self.l.addWidget(self.accplot_channels[-1], i, 1, 1, 2)

        self.refreshRate = 0.05
        
        self.acccurve = []
        for i in range(ACC_RANGE):
            c = self.accplot_channels[i].plot(pen=(i,10))
            c.setPos(0,0)
            self.acccurve.append(c)
        
        self.lastUpdateTime = time.time()
        
        self.window_type = 'acc'
    
    def ori_plots(self):
        self.cw.close()
        
        self.cw = QtGui.QWidget()
        self.setCentralWidget(self.cw)
        self.l = QtGui.QGridLayout()
        self.cw.setLayout(self.l)
        
        titleLabel = QtGui.QLabel('Myo Data Acquirer')
        titleLabel.setFont(QtGui.QFont("Garamond", 16, QtGui.QFont.Bold))
        self.l.addWidget(titleLabel, 0, 0, 2, 1)
        
        all_button = QtGui.QPushButton('All Plots')
        all_button.setToolTip('Open all plots.')
        all_button.clicked.connect(self.revert_to_all_plots)
        self.l.addWidget(all_button, 0, 0, 1, 1)
        
        record = QtGui.QPushButton('Record Data')
        record.setToolTip('Record MYO Data')
        record.setStyleSheet("background-color: green")
        record.clicked.connect(self.toggle_record)
        self.record = record
        self.l.addWidget(record, 1, 0, 1, 1)
        
        self.oriplot_channels = []
        for i in range(ORI_RANGE):
                
            self.oriplot_channels.append(pg.PlotWidget(name='Orientation Channel %s' % (i+1)))
            self.oriplot_channels[-1].setRange(QtCore.QRectF(0,-1,1000,8))
            self.oriplot_channels[-1].disableAutoRange()
            self.oriplot_channels[-1].setTitle("Orientation Channel %s" % (i+1))
            self.l.addWidget(self.oriplot_channels[-1], i, 1, 1, 2)

        self.refreshRate = 0.05
        
        self.oricurve = []
        for i in range(ORI_RANGE):
            c = self.oriplot_channels[i].plot(pen=(i,10))
            c.setPos(0,0)
            self.oricurve.append(c)
        
        self.lastUpdateTime = time.time()
        
        self.window_type = 'ori'
        
    def toggle_record(self):
        if self.myo_data_record.recording:
            filename = self.myo_data_record.save_record()
            print('Record saved at %s' % filename)
            
            self.record.setStyleSheet("background-color: green")
            self.record.setText("Record Data")
            self.record.setToolTip('Record MYO Data')
        else:
            self.record.setStyleSheet("background-color: red")
            self.record.setText("Stop Recording")
            self.record.setToolTip('Stop Recording MYO Data')
            
        self.myo_data_record.toggle_recording()
        #
        
    def start_listening(self):
        self.myo_data_record = data_collector.myo_data_collector()
        self.listener = Listener(self)
        self.hub = libmyo.Hub()
        self.hub.set_locking_policy(libmyo.LockingPolicy.none)
        self.hub.run(1000, self.listener)

    def update_plots(self):
        ctime = time.time()
        
        win = self.window_type
        
        if (ctime - self.lastUpdateTime) >= self.refreshRate:
            self.myo_data_record.collect(self.listener, ctime)
            if win == 'all' or win == 'emg':
                for i in range(EMG_RANGE):
                    try:
                        self.emgcurve[i].setData(self.listener.emg.data[i,:])
                    except IndexError as e1:
                        print('EMG CURVE LEN:', len(self.emgcurve))
                        print('LISTENER EMG DATA CHANNEL LEN:', len(self.listener.emg.data))
                        print('LISTENER EMG DATA STREAM LEN:', len(self.listener.emg.data[i]))
                        print('Current Index:', i)
            if win == 'all' or win == 'ori':
                for i in range(ORI_RANGE):
                    self.oricurve[i].setData(self.listener.orientation.data[i,:])
            if win == 'all' or win == 'acc':
                for i in range(ACC_RANGE):
                    self.acccurve[i].setData(self.listener.acc.data[i,:])
                
            self.lastUpdateTime = ctime
            app.processEvents()
        
    def closeEvent(self, event, restart=0):
        print("Closing...")
        self.hub.shutdown()
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = RawWindow()
    sys.exit(app.exec_())
