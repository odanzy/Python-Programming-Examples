# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import visa
import tkinter
from tkinter import messagebox

# Hide main tkinter window
root = tkinter.Tk()
root.withdraw()

rm = visa.ResourceManager()

na = rm.open_resource('TCPIP0::141.121.210.126::inst0::INSTR')

print (na.query('*IDN?'))

na.write('SYST:FPR')

na.write('CALC:CUST:DEF "myVC21", "Vector Mixer/Converter", "VC21"')
na.write('DISP:WIND1:STAT ON')
na.write('DISP:WIND1:TRAC1:FEED "myVC21"')

na.write('ROUT:PATH:LOOP:R1 EXT')

mxrfile = '\'D:\\myDummyMixer.mxrx\''
mxrcalfile = '\'D:\\Dummy_Mixer001.s2px\''


na.write('SENS:MIX:LOAD')

na.write('SENS:CORR:COLL:SESS:INIT "VMC"')
na.write('SENS:CORR:COLL:SESS:VMC:OPER "CAL"')
na.write('SENS:CORR:COLL:SESS:VMC:TWOP:OPT "MECH"')
na.write('SENS:CORR:COLL:SESS:VMC:MIX:CHAR:CAL:OPT FILE,' + mxrcalfile)

mixerOpt = na.query('SENS:CORR:COLL:SESS:VMC:MIX:CHAR:CAL:OPT?')
print('Mixer Cal Option = ' + mixerOpt)

calFile = na.query('SENS:CORR:COLL:SESS:VMC:MIX:CHAR:CAL:FIL?')
print('Mixer Cal File = ' + calFile)

na.write('SENS:CORR:COLL:SESS:CONN:PORT1:SEL "APC 3.5 male"')
na.write('SENS:CORR:COLL:SESS:CONN:PORT2:SEL "APC 3.5 female"')
na.write('SENS:CORR:COLL:SESS:CKIT:PORT1:SEL "85052D"')
na.write('SENS:CORR:COLL:SESS:CKIT:PORT2:SEL "85052D"')

na.write('SENS:CORR:COLL:SESS:VMC:TWOP:METH "DEFAULT"')
na.write('SENS:CORR:COLL:SESS:VMC:TWOP:OMIT 1')

na.write('SENS:CORR:COLL:SESS:STEP')
numSteps = na.query('SENS:CORR:COLL:SESS:STEP?')
print('Number of Cal Steps = ' + numSteps)

for j in range(1,int(numSteps)+1):
    messagebox.showinfo('Cal Step ' + str(j) + ' of ' + str(int(numSteps)) ,na.query('SENS:CORR:COLL:SESS:DESC? ' + str(j)))    
    na.write('SENS:CORR:COLL:SESS:ACQ ' + str(j))

na.write('SENS:CORR:COLL:SESS:SAVE?')

messagebox.showinfo('VMC Cal Complete')

na.close()
rm.close()