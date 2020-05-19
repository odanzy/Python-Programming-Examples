import visa
import tkinter
from tkinter import messagebox

# Hide main tkinter window
root = tkinter.Tk()
root.withdraw()

rm = visa.ResourceManager()

na = rm.open_resource('TCPIP0::localhost::inst0::INSTR')

print (na.query('*IDN?'))

na.write('SYST:FPR')

na.write('CALC:CUST:DEF "myVC21", "Vector Mixer/Converter", "VC21"')
na.write('DISP:WIND1:STAT ON')
na.write('DISP:WIND1:TRAC1:FEED "myVC21"')

na.write('ROUT:PATH:LOOP:R1 EXT')

#mxrfile = '\'D:\\myDummyMixer.mxrx\''
mxrcalfile = '\'D:\\Dummy_Mixer001.s2px\''

na.write('SENS:CORR:COLL:SESS:INIT "VMC"')

## Select either mixer characterization or full calibration
na.write('SENS:CORR:COLL:SESS:VMC:OPER "CHAR"')
#na.write('SENS:CORR:COLL:SESS:VMC:OPER "CAL"')

## Select either to use mechanical standards or ecal
na.write('SENS:CORR:COLL:SESS:VMC:TWOP:OPT "MECH"')
na.write('SENS:CORR:COLL:SESS:VMC:MIX:CHAR:CAL:OPT MECH')
# na.write('SENS:CORR:COLL:SESS:VMC:TWOP:OPT "ECAL"')
# na.write('SENS:CORR:COLL:SESS:VMC:MIX:CHAR:CAL:OPT ECAL')

## Set name to store characterized mixer data
na.write('SENS:CORR:COLL:SESS:VMC:MIX:CHAR:CAL:FIL ' + mxrcalfile)

mixerOpt = na.query('SENS:CORR:COLL:SESS:VMC:MIX:CHAR:CAL:OPT?')
print('Mixer Cal Option = ' + mixerOpt)

calFile = na.query('SENS:CORR:COLL:SESS:VMC:MIX:CHAR:CAL:FIL?')
print('Mixer Cal File = ' + calFile)


## Port Selection (port 1 is mixer input and port 3 is mixer output) - for full calibration, port 2 would also need to be defined.
na.write('SENS:CORR:COLL:SESS:CONN:PORT1:SEL "APC 3.5 female"')
na.write('SENS:CORR:COLL:SESS:CONN:PORT3:SEL "APC 3.5 male"')

## Ecal selection when using ecal (must also select port and which characterization)
#na.write('SENS:CORR:COLL:SESS:VMC:MIX:ECAL:CHAR 1,0')
#na.write('SENS:CORR:COLL:SESS:VMC:MIX:ECAL:PORT 1,"A1"')

## Cal Kit Selection for mechanical cal kits
na.write('SENS:CORR:COLL:SESS:CKIT:PORT1:SEL "85052D"')
na.write('SENS:CORR:COLL:SESS:CKIT:PORT3:SEL "85052D"')

## Set Thru path method (required for full calibration process)
na.write('SENS:CORR:COLL:SESS:VMC:TWOP:METH "DEFAULT"')
na.write('SENS:CORR:COLL:SESS:VMC:TWOP:OMIT 1')

## Calculate the number of calibration steps
na.write('SENS:CORR:COLL:SESS:STEP')
numSteps = na.query('SENS:CORR:COLL:SESS:STEP?')
print('Number of Cal Steps = ' + numSteps)


## Complete the calibration process
for j in range(1,int(numSteps)+1):
    messagebox.showinfo('Cal Step ' + str(j) + ' of ' + str(int(numSteps)) ,na.query('SENS:CORR:COLL:SESS:DESC? ' + str(j)))    
    na.write('SENS:CORR:COLL:SESS:ACQ ' + str(j))
    opc=na.query('*OPC?')

## Finalize calibration
na.write('SENS:CORR:COLL:SESS:SAVE?')

messagebox.showinfo('VMC Cal Complete', 'VMC Cal Complete')


## Close sessions
na.close()
rm.close()
