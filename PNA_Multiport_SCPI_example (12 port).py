#import pyvisa.visa library
import visa

drm = visa.ResourceManager()

#Create a connection to instrument
na=drm.open_resource("TCPIP0::141.121.210.126::hislip0::INSTR")

#Get IDN String back from instrument and display on screen
print(na.ask("*IDN?"))

#Preset PNA
# na.write(":SYST:PRES; *OPC?;")
# opc=na.read()

#Delete all existing measurements
na.write(":CALC:MEAS:DEL:ALL")

#Make sure that Window 1 is on
na.write(":DISP:WIND1:STAT ON")

#Create a SDD11 measurement - The sequence below first creates a S11 
#measurement, displays it on the window
na.write(":CALC1:MEAS1:DEF 'S11'")
na.write(":DISP:MEAS1:FEED 1")

#This creates 6 differential ports using ports 1-12 
#(1-2 = port 1, 3-4 = port 2, etc..).  After sending this command you can make
#changes through the GUI as well and add other parameters.
na.write(":CALC1:DTOP 'BBBBBB', 1,3,2,4,5,7,6,8,9,11,10,12")

#Convert existing 1st measurement (S11) to be SDD11
na.write(":CALC1:MEAS1:PAR 'SDD11'")

#Create a SDD66 measurement.  This follows the same process as above, but 
#there is no need to define the ports as differential again as they are 
#are already defined
na.write(":CALC1:MEAS2:DEF 'S11'")
na.write("CALC1:MEAS2:PAR 'SDD66'")
na.write(":DISP:MEAS2:FEED 1")

#Set timeout to 10s
na.timeout=10000

#Trigger and wait for a single sweep
na.write(":SENS:SWE:MODE SING; *OPC?")
opc=na.read()
print("Sweep Complete")

#Save a Single-Ended Touchstone File
#Set Measurement 1 back to a single ended parameter so that the save command will process as single-ended
na.write(":CALC1:MEAS1:PAR 'S11'")
na.write(":CALC1:DATA:SNP:PORT:SAVE '1,2,3,4,5,6,7,8,9,10,11,12','D:\\test.s12p'")
opc=na.query("*OPC?")
print("Save Complete")

#Set measurement back to SDD11
na.write(":CALC1:MEAS1:PAR 'SDD11'")

