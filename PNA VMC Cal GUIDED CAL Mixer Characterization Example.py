# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import visa
import tkinter
from tkinter import messagebox

root = tkinter.Tk()
root.withdraw()

rm = visa.ResourceManager()

na = rm.open_resource('TCPIP0::141.121.210.109::hislip0::INSTR')

print (na.query('*IDN?'))

na.write('SYST:FPR')

na.write('CALC:CUST:DEF "myVC21", "Vector Mixer/Converter", "VC21"')
na.write('DISP:WIND1:STAT ON')
na.write('DISP:WIND1:TRAC1:FEED "myVC21"')

na.write('ROUT:PATH:LOOP:R1 EXT')

mxrfile = '\'D:\\myDummyMixer.mxrx\''
mxrcalfile = '\'D:\\Dummy_Mixer001.s2px\''


#na.write('SENS:MIX:LOAD ' + mxrfile)
na.write('SENS:CORR:COLL:GUID:VMC:OPER "CHAR"') #DOESN'T WORK
#na.write('SENS:CORR:COLL:GUID:VMC:OPER "CAL"') #WORKS

na.write('SENS:CORR:COLL:GUID:VMC:MIX:CHAR:CAL:OPT CKIT')
#na.write('SENS:CORR:COLL:GUID:VMC:MIX:CHAR:CAL:OPT FILE,' + mxrcalfile)

mixerOpt = na.query('SENS:CORR:COLL:GUID:VMC:MIX:CHAR:CAL:OPT?')
print('Mixer Cal Option = ' + mixerOpt)

calFile = na.query('SENS:CORR:COLL:GUID:VMC:MIX:CHAR:CAL:FIL?')
print('Mixer Cal File = ' + calFile)

na.write('SENS:CORR:COLL:GUID:CONN:PORT1 "APC 3.5 female"')
na.write('SENS:CORR:COLL:GUID:CONN:PORT2 "APC 3.5 male"')
na.write('SENS:CORR:COLL:GUID:CKIT:PORT1 "85052D"')
na.write('SENS:CORR:COLL:GUID:CKIT:PORT2 "85052D"')

#na.write('SENS:CORR:COLL:SESS:VMC:TWOP:METH "DEFAULT"')
#na.write('SENS:CORR:COLL:SESS:VMC:TWOP:OMIT 1')

na.write('SENS:CORR:COLL:GUID:INIT')
numSteps = na.query('SENS:CORR:COLL:GUID:STEPS?')
print('Number of Cal Steps = ' + numSteps)

for j in range(0,int(numSteps)):
    messagebox.showinfo('Cal Step ' + str(j) + ' of ' + str(int(numSteps)-1) ,na.query('SENS:CORR:COLL:SESS:DESC? ' + str(j)))    
    na.write('SENS:CORR:COLL:GUID:ACQ STAN' + str(j+1))

na.write('SENS:CORR:COLL:GUID:SAVE')

messagebox.showinfo('VMC Cal Complete')

na.close()
rm.close()
