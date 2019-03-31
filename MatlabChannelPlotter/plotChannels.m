%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   Author: Chris Angelini
%
%   Porpoise: Uses a GUI to initalize the Myo Band and streams data from 
%     ;)     the Myo Band and plots the channels separately in realtime
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function varargout = plotChannels(varargin)
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @plotChannels_OpeningFcn, ...
                   'gui_OutputFcn',  @plotChannels_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before plotChannels is made visible.
function plotChannels_OpeningFcn(hObject, eventdata, handles, varargin)
global mm m1 const updateTimer m2 
handles.FIGchannelPlot.Visible = 'off';
% Choose default command line output for plotChannels
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

currDir = pwd;
% imageDir = [ '\Images\'];
myImage = imread(['logo.png']);
axes(handles.AXElogo);
imshow(myImage);

set(handles.AXEchannels1.XAxis, 'Visible','off')
set(handles.AXEchannels1.YAxis, 'Visible','off')
set(handles.AXEchannels1, 'Color',[1 1 1])
% title(handles.AXEchannels1,'EMG Channel 1');

set(handles.AXEchannels2.XAxis, 'Visible','off')
set(handles.AXEchannels2.YAxis, 'Visible','off')
set(handles.AXEchannels2, 'Color',[1 1 1])
% title(handles.AXEchannels2,'EMG Channel 2');

set(handles.AXEchannels3.XAxis, 'Visible','off')
set(handles.AXEchannels3.YAxis, 'Visible','off')
set(handles.AXEchannels3, 'Color',[1 1 1])
% title(handles.AXEchannels3,'EMG Channel 3');

set(handles.AXEchannels4.XAxis, 'Visible','off')
set(handles.AXEchannels4.YAxis, 'Visible','off')
set(handles.AXEchannels4, 'Color',[1 1 1])

set(handles.AXEchannels5.XAxis, 'Visible','off')
set(handles.AXEchannels5.YAxis, 'Visible','off')
set(handles.AXEchannels5, 'Color',[1 1 1])

set(handles.AXEchannels6.XAxis, 'Visible','off')
set(handles.AXEchannels6.YAxis, 'Visible','off')
set(handles.AXEchannels6, 'Color',[1 1 1])

set(handles.AXEchannels7.XAxis, 'Visible','off')
set(handles.AXEchannels7.YAxis, 'Visible','off')
set(handles.AXEchannels7, 'Color',[1 1 1])

set(handles.AXEchannels8.XAxis, 'Visible','off')
set(handles.AXEchannels8.YAxis, 'Visible','off')
set(handles.AXEchannels8, 'Color',[1 1 1])
% title(handles.AXEchannel4,'EMG Channel 7');

set(handles.FIGchannelPlot, 'DeleteFcn', @plotChannels_ClosingFcn)
handles.FIGchannelPlot.Visible = 'on';

% UIWAIT makes plotChannels wait for user response (see UIRESUME)
% uiwait(handles.FIGchannelPlot);

function plotChannels_ClosingFcn(hObject, eventdata, handles) 
global mm m1 const updateTimer m2 
if exist('mm','var')
    if m1.isStreaming() == 1 
        m1.stopStreaming();
    end
    mm.delete;
    disp('Kill')
    clear mm
    delete(updateTimer)
    
end

% --- Outputs from this function are returned to the command line.
function varargout = plotChannels_OutputFcn(hObject, eventdata, handles) 
global mm m1 const updateTimer
varargout{1} = handles.output;

% --- Executes on button press in BTNinit.
function BTNinit_Callback(hObject, eventdata, handles)
global mm m1 const updateTimer m2
handles.BTNinit.Enable = 'off';

pause(0.1)

warning('off')
% addpath('C:\myo-sdk-win-0.9.0\bin');
% addpath(genpath('C:\Users\chris\Documents\GraduateWork\Prosthetics\mark-toma-MyoMex-6a6a0d5'))

install_myo_mex

sdk_path = '..\myo-sdk-win-0.9.0'; % root path to Myo SDK
build_myo_mex(sdk_path);


mm = [];
m1 = [];
const = struct;


mm = MyoMex(1);

m1 = mm.myoData(1);

pause(0.1);
const.Frequency = 200;
const.UpdateRate = 10;
const.UpdateStartDelay = 1;
const.StripYLimit = [-1.2,1.2];

% updateTimer = timer('name','MyoMexGUI_Monitor_update_timer',...
%                               'busymode','drop',...
%                               'executionmode','fixedrate',...
%                               'period',1/const.UpdateRate,...
%                               'startdelay',const.UpdateStartDelay,...
%                               'timerfcn',@(src,evt)updateFigureCallback(hObject, eventdata, handles));

m1.timeEMG
m1.emg

handles.BTNstart.Enable = 'on';
handles.BTNstop.Enable = 'on';

function updateFigureCallback(hObject, eventdata, handles)
global mm m1 m2 const updateTimer
plot(handles.AXEchannels1,1:201,m1.emg_log(end-200:end,1),'Color','b','LineWidth',2);
set(handles.AXEchannels1,'ylim',const.StripYLimit,'xlim', [0 200],'Color',[0 0 0],'xTickLabel',[]);

plot(handles.AXEchannels2,1:201,m1.emg_log(end-200:end,2),'Color','r','LineWidth',2);
set(handles.AXEchannels2,'ylim',const.StripYLimit,'xlim', [0 200],'Color',[0 0 0],'xTickLabel',[]);

plot(handles.AXEchannels3,1:201,m1.emg_log(end-200:end,3),'Color','g','LineWidth',2);
set(handles.AXEchannels3,'ylim',const.StripYLimit,'xlim', [0 200],'Color',[0 0 0],'xTickLabel',[]);

plot(handles.AXEchannels4,1:201,m1.emg_log(end-200:end,4),'Color','b','LineWidth',2);
set(handles.AXEchannels4,'ylim',const.StripYLimit,'xlim', [0 200],'Color',[0 0 0],'xTickLabel',[]);

plot(handles.AXEchannels5,1:201,m1.emg_log(end-200:end,5),'Color','b','LineWidth',2);
set(handles.AXEchannels5,'ylim',const.StripYLimit,'xlim', [0 200],'Color',[0 0 0],'xTickLabel',[]);

plot(handles.AXEchannels6,1:201,m1.emg_log(end-200:end,6),'Color','r','LineWidth',2);
set(handles.AXEchannels6, 'ylim',const.StripYLimit,'xlim', [0 200],'Color',[0 0 0],'xTickLabel',[]);

plot(handles.AXEchannels7,1:201,m1.emg_log(end-200:end,7),'Color','g','LineWidth',2);
set(handles.AXEchannels7,'ylim',const.StripYLimit,'xlim', [0 200],'Color',[0 0 0],'xTickLabel',[]);

plot(handles.AXEchannels8,1:201,m1.emg_log(end-200:end,8),'Color','b','LineWidth',2);
set(handles.AXEchannels8,'ylim',const.StripYLimit,'xlim', [0 200],'Color',[0 0 0],'xTickLabel',[]);


% --- Executes on button press in BTNstart.
function BTNstart_Callback(hObject, eventdata, handles)
global mm m1 const updateTimer m2
const.Frequency = 5;
% hObject    handle to BTNstart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUI+
m1.startStreaming();
tic
x = 1;
while x > 0
    x = x +1;
    stamp = toc;
    if stamp<x/const.Frequency
        pause(x/const.Frequency-stamp)
        try
            updateFigureCallback(hObject, eventdata, handles)
        catch
        end
    end
end



% --- Executes on button press in BTNstop.
function BTNstop_Callback(hObject, eventdata, handles)
global mm m1 const updateTimer m2
% hObject    handle to BTNstop (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
m1.stopStreaming();
stop(updateTimer);
