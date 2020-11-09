"""
@brief The system scans a 3D space with user-defined parameters to
create 3D graphs of electromagnetic fields for wireless power systems.

@authors: usmank13, chasewhyte, Tri Nguyen

"""

import numpy as np
import serial
import time
import random
import visa
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt 
from matplotlib import cm
from matplotlib import colors
from matplotlib.ticker import FuncFormatter
from VNAFunctions import *
from ButtonFunctions import *

# Creating a Window of the Application
window = Tk()
window.title("3DEVS")

# tabs controlling and graphing
tab_ctrl = ttk.Notebook(window)
VNATab = ttk.Frame(tab_ctrl)
GraphTab = ttk.Frame(tab_ctrl)
tab_ctrl.add(VNATab, text = 'System Control')
tab_ctrl.add(GraphTab, text = 'Graphing Data')
tab_ctrl.pack(expand= True, fill='both')

#IN the System Control Tab
#Sectionin of Tilt and Pan, VNA-MPCNC, and Future Live Scan
Tilt_Pan = ttk.LabelFrame(VNATab, text = 'Tilt and Pan')
Tilt_Pan.pack(fill=BOTH, expand=True, side = 'left')
MPCNC = ttk.LabelFrame(VNATab, text = 'VNA')
MPCNC.pack(fill=BOTH, expand=True,side = 'left')
Live_Panel = ttk.LabelFrame(VNATab, text = 'Live View')
Live_Panel.pack(fill = BOTH, expand = True, side = 'left')

# IN the Graphing Tab
name =  ttk.LabelFrame(GraphTab, text = 'FILE NAME')
name.pack(fill = BOTH, expand = False)
Parameters = ttk.LabelFrame(GraphTab, text = 'PARAMETER SELECTIONS')
Parameters.pack(fill=BOTH, expand=True)

#In the Pan and Tilt Tab

# Labeling of the components
tilt_lbl = Label(Tilt_Pan, text = "Tilt Servo Angle (0-90):")
tilt_lbl.grid(row = 1, column = 0)
tilt_txt = Entry(Tilt_Pan, width = 10, state = 'normal')
tilt_txt.grid(row = 1, column = 1)
tilt_confm_lbl = Label(Tilt_Pan, text = "")
tilt_confm_lbl.grid(row = 1, column = 3)

pan_lbl = Label(Tilt_Pan, text = "Pan Servo Angle (20-160): ")
pan_lbl.grid(row = 2, column = 0)
pan_txt = Entry(Tilt_Pan, width = 10, state = 'disabled')
pan_txt.grid(row = 2, column = 1)
pan_confm_lbl = Label(Tilt_Pan, text = "")
pan_confm_lbl.grid(row = 2, column = 3)

################################################# THE VNA-MPCNC TAB

#VNA-MPCNC tab's components set up
lbl00 = Label(MPCNC, text = "Length: ")
lbl00.grid(row = 0, column = 0)
txt00 = Entry(MPCNC, width = 10)
txt00.grid(row = 0, column = 1)

lbl01 = Label(MPCNC, text = "Width:")
lbl01.grid(row = 1, column = 0)
txt01 = Entry(MPCNC, width = 10)
txt01.grid(row = 1, column = 1)

lbl02 = Label(MPCNC, text = "Pause duration (s): ")
lbl02.grid(row = 2, column = 0)
txt02 = Entry(MPCNC, width = 10)
txt02.grid(row = 2, column = 1)

lbl03 = Label(MPCNC, text = "xStep: ") ## used to be samplingF
lbl03.grid(row = 3, column = 0)
txt03 = Entry(MPCNC, width = 10)
txt03.grid(row = 3, column = 1)

lbl04 = Label(MPCNC, text = "yStep: ")
lbl04.grid(row = 4, column = 0)
txt04 = Entry(MPCNC, width = 10)
txt04.grid(row = 4, column = 1)

lbl05 = Label(MPCNC, text = "Height: ") # used to be called depth
lbl05.grid(row = 5, column = 0)
txt05 = Entry(MPCNC, width = 10)
txt05.grid(row = 5, column = 1)

# lbl06 = Label(MPCNC, text = "Center Frequency: ")
# lbl06.grid(row = 6, column = 0)
# txt06 = Entry(MPCNC, width = 10)
# txt06.grid(row = 6, column = 1)

lbl07 = Label(MPCNC, text = "Center Frequency: ")
lbl07.grid(row = 6, column = 0)
txt07 = Entry(MPCNC, width = 10)
txt07.grid(row = 6, column = 1)

lbl08 = Label(MPCNC, text = "Span: ")
lbl08.grid(row = 7, column = 0)
txt08 = Entry(MPCNC, width = 10)
txt08.grid(row = 7, column = 1)

lbl09 = Label(MPCNC, text = "Number of Points: ")
lbl09.grid(row = 8, column = 0)
txt09 = Entry(MPCNC, width = 10)
txt09.grid(row = 8, column = 1)

lbl10 = Label(MPCNC, text = "Z-Step: ")
lbl10.grid(row = 9, column = 0)
txt10 = Entry(MPCNC, width = 10)
txt10.grid(row = 9, column = 1)

lbl11 = Label(MPCNC, text = "Name the File: ")
lbl11.grid(row = 10, column = 0)
txt11 = Entry(MPCNC, width = 10)
txt11.grid(row = 10, column = 1)
'''
# setting up the drop down menu for is youre using tilt and pan or not
# ArduinoVar =StringVar(Tilt_Pan)
# ArduinoVar.set("No")
# arduinoPort = False
# ArduinoOpt = OptionMenu(Tilt_Pan, ArduinoVar, "No", "Yes")
# ArduinoOpt.grid(row = 0, column = 0, padx = 20, pady = 10 )

# def clicked0():
# 	if ArduinoVar == "Yes":
# 		arduinoPort = True
# 		arduino = serial.Serial('COM53', 9600) #Com port is subjected to changee

# ArduinoButt = Button(Tilt_Pan, text= 'SEND', command = clicked0)
# ArduinoButt.grid(row = 0, column = 1)

#this line opens arduino port
#arduino = serial.Serial('COM53', 9600) #Com port is subjected to change
'''
#HANDLER FUNCTIONS
def Handlerclicked1():
    clicked1(tilt_txt, tilt_confm_lbl, pan_txt)
def Handlerclicked2():
    clicked2(pan_txt,pan_confm_lbl,reset_btn)
def Handlerrun_vna():
    run_vna(reset_VNA,start_btn,txt00,txt01,txt02,txt03,txt04,txt05,txt07,txt08,txt09,txt10,txt11, MPCNC)
def Handlerresets():
    resets(reset_btn, tilt_txt)
def Handlersubmit_values():
    submit_values(submit_val,start_btn,reset_btn,txt00,txt01,txt02,txt03,txt04,txt05,txt07,txt08,txt09,txt10,txt11)
def HandlerVNAreset():
    VNAreset(reset_VNA,submit_val,txt00,txt01,txt02,txt03,txt04,txt05,txt07,txt08,txt09,txt10,txt11)
    
 # Button layouts
tilt_btn1 = Button(Tilt_Pan, text= 'SEND', command = Handlerclicked1)
tilt_btn1.grid(row = 1, column = 2)

pan_btn1 = Button(Tilt_Pan, text= 'SEND', command = Handlerclicked2)
pan_btn1.grid(row = 2, column = 2)

reset_btn = Button(Tilt_Pan, text="RESET", command = Handlerresets, state = 'disabled',  bg="red", fg="black", font = 'Helvetica 18 bold')
reset_btn.grid(row = 3, column = 2, pady = 30)


submit_val = Button(MPCNC, text = 'SUBMIT VALUES', command = Handlersubmit_values, font = 'Helvetica 10 bold')
submit_val.grid(row = 12, column = 1, padx = 5, pady = 5)

reset_VNA = Button(MPCNC, text = 'RESET VALUES', command = HandlerVNAreset, state = 'disabled', font = 'Helvetica 10 bold')
reset_VNA.grid(row = 13, column = 1, padx = 5, pady = 5)

#initialize the timer
hours_took = 0

"""
VNA FUNCTION CALL HERE
"""
start_btn = Button(MPCNC, text= 'SEND', command = Handlerrun_vna, bg="green", fg="black", font = 'Helvetica 18 bold')
start_btn.grid(row = 14, column = 1, padx = 10, pady = 10)

##################################### GRAPHING

# Setting up layout
file_name = Label(name, text = "File Name:")
file_name.grid(row = 0, column = 0)
file_txt = Entry(name, width = 20, state = 'normal')
file_txt.grid(row = 0, column = 1)

# setting up buttons
def send():
	file_txt.configure(state = 'disabled')

btnSend = Button(name, text = 'SUBMIT', command = send, state = 'normal', bg = 'green', fg = 'black')
btnSend.grid(row = 0, column = 2, padx = 10, pady = 5)

def reset_graph():
	file_txt.configure(state = 'normal')

btnSend = Button(name, text = 'RESET', command = reset_graph, state = 'normal', bg = 'red', fg = 'black')
btnSend.grid(row = 0, column = 3, padx = 10, pady = 5)


def S11Param():
    filename_input = file_txt.get()
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection = '3d')
    x, y, z, s11, s12, s21, s22 = np.loadtxt(filename_input + '.txt', delimiter = ",", unpack = True) 
    ax1.set_title('S11')
    ax1.set_xlabel('X Position (mm)')
    ax1.set_ylabel('Y Position (mm)')
    ax1.set_zlabel('Z Position (mm)')
    p = ax1.scatter(x, y, z, c = s11, cmap = 'jet')
    colorbar = fig.colorbar(p)
    colorbar.set_label('Decibels')
    plt.show()

s11 = Button(Parameters, text= 'S11', command = S11Param, state = 'normal', bg="green", fg="black", font = 'Helvetica 18 bold')
s11.grid(row = 0, column = 0, padx = 10, pady = 5)

def S12Param():
    filename_input = file_txt.get()
    # s12.configure(state = 'disabled')
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection = '3d')
    x, y, z, s11, s12, s21, s22 = np.loadtxt(filename_input + '.txt', delimiter = ",", unpack = True) 
    ax1.set_title('S12')
    ax1.set_xlabel('X Position (mm)')
    ax1.set_ylabel('Y Position (mm)')
    ax1.set_zlabel('Z Position (mm)')
    p = ax1.scatter(x, y, z, c = s12, cmap = 'jet')
    colorbar = fig.colorbar(p)
    colorbar.set_label('Decibels')
    plt.show()

s12 = Button(Parameters, text= 'S12', command = S12Param, state = 'normal', bg="green", fg="black", font = 'Helvetica 18 bold')
s12.grid(row = 0, column = 2, padx = 10, pady = 5)

def S22Param():
    filename_input = file_txt.get()
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection = '3d')
    x, y, z, s11, s12, s21, s22 = np.loadtxt(filename_input + '.txt', delimiter = ",", unpack = True) 
    ax1.set_title('S22')
    ax1.set_xlabel('X Position (mm)')
    ax1.set_ylabel('Y Position (mm)')
    ax1.set_zlabel('Z Position (mm)')
    p = ax1.scatter(x, y, z, c = s22, cmap = 'jet')
    colorbar = fig.colorbar(p)
    colorbar.set_label('Decibels')
    plt.show()

s22 = Button(Parameters, text= 'S22', command = S22Param, state = 'normal', bg="green", fg="black", font = 'Helvetica 18 bold')
s22.grid(row = 0, column = 4, padx = 10, pady = 5)

def S21Param():
    filename_input = file_txt.get()
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection = '3d')
    x, y, z, s11, s12, s21, s22 = np.loadtxt(filename_input + '.txt', delimiter = ",", unpack = True) 
    ax1.set_title('S21')
    ax1.set_xlabel('X Position (mm)')
    ax1.set_ylabel('Y Position (mm)')
    ax1.set_zlabel('Z Position (mm)')
    p = ax1.scatter(x, y, z, c = s21, cmap = 'jet')
    colorbar = fig.colorbar(p)
    colorbar.set_label('Decibels')
    plt.show()

s21 = Button(Parameters, text= 'S21', command = S21Param, state = 'normal', bg="green", fg="black", font = 'Helvetica 18 bold')
s21.grid(row = 0, column = 6, padx = 10, pady = 5)


# NOTE: I think some of this is redundant, will need to test removing it and seeing if everything works okay. 
################################# Live View stuff (very similar to the graphing tab careful not to edit the wrong one)

def S11Param():
    ##### put the funtion that will generate each point here
    print('temporary placement action')

s11 = Button(Live_Panel, text= 'S11', command = S11Param, state = 'normal', bg="green", fg="black", font = 'Helvetica 18 bold')
s11.grid(row = 0, column = 0, padx = 10, pady = 5)

def S12Param():
    ##### put the funtion that will generate each point here
    print('temporary placement action')

s12 = Button(Live_Panel, text= 'S12', command = S12Param, state = 'normal', bg="green", fg="black", font = 'Helvetica 18 bold')
s12.grid(row = 0, column = 2, padx = 10, pady = 5)

def S22Param():
    ##### put the funtion that will generate each point here
    print('temporary placement action')

s22 = Button(Live_Panel, text= 'S22', command = S22Param, state = 'normal', bg="green", fg="black", font = 'Helvetica 18 bold')
s22.grid(row = 0, column = 4, padx = 10, pady = 5)

def S21Param():
    ##### put the funtion that will generate each point here
    print('temporary placement action')

s21 = Button(Live_Panel, text= 'S21', command = S21Param, state = 'normal', bg="green", fg="black", font = 'Helvetica 18 bold')
s21.grid(row = 0, column = 6, padx = 10, pady = 5)


######################### end of code

window.mainloop()
