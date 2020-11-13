
"""
@brief: Functionality for GUI buttons

@author: chasewhyte
"""
import time
'''
# setting up the drop down menu for is youre using tilt and pan or not
# ArduinoVar =StringVar(Tilt_Pan)
# ArduinoVar.set("No")
# arduinoPort = False
# ArduinoOpt = OptionMenu(Tilt_Pan, ArduinoVar, "No", "Yes")
# ArduinoOpt.grid(row = 0, column = 0, padx = 20, pady = 10 )

# def clicked0():
#     if ArduinoVar == "Yes":
#         arduinoPort = True
#         arduino = serial.Serial('COM53', 9600) #Com port is subjected to changee

# ArduinoButt = Button(Tilt_Pan, text= 'SEND', command = clicked0)
# ArduinoButt.grid(row = 0, column = 1)

#this line opens arduino port
#arduino = serial.Serial('COM53', 9600) #Com port is subjected to change
'''

# Defines functionality for the tilt button
# Sends messages to the user upon a click and sends command to the tilt motor
def tp_head_tilt(tilt_txt, tilt_confm_lbl, pan_txt, ser_tp_head):
    res1 = tilt_txt.get()
    if (int(res1) > 89):
        tilt_confm_lbl.configure(text = "Must be 0-89 degrees")
    else:
        tilt_confm_lbl.configure(text = "Sent " + res1 + " Tilt Angle")
        tilt_txt.configure(state = 'disabled')
        pan_txt.configure(state = 'normal')
        res1 = (str(res1).encode())
#         arduino.write(res1)
        ser_tp_head.write(res1)


# Defines functionality for the pan button
# Sends messages to the user upon a click on the pan button and sends command to the pan motor
def tp_head_pan(pan_txt,pan_confm_lbl,reset_btn, ser_tp_head):
    res2 = pan_txt.get()
    if (int(res2) < 20 and int(res2) > 160):
        pan_confm_lbl.configure(text = "Must be 20-160 degress")
    else:
        pan_confm_lbl.configure(text = "Sent " + res2 + " Pan Angle")
        pan_txt.configure(state = 'disabled')
        reset_btn.configure(state = 'normal')
        res2 = (str(res2).encode())
#         arduino.write(res2)
        ser_tp_head.write(res2)

# Resets tilt and pan motor state
def tp_head_resets(reset_btn, tilt_txt, ser_tp_head):
    reset_btn.configre(state = 'disabled')
#     arduino.write('0'.encode())
    ser_tp_head.write('0'.encode())
    time.sleep(2)
#     arduino.write('20'.encode())
    ser_tp_head.write('20'.encode())
    time.sleep(2)
    tilt_txt.configure(state = 'normal')
    