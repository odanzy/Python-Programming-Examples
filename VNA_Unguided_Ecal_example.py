#import pyvisa.visa library
import visa

drm = visa.ResourceManager()

#Create a connection to instrument
na=drm.open_resource("TCPIP0::141.121.210.109::hislip0::INSTR")

#Get IDN String back from instrument and display on screen
print(na.query("*IDN?").strip())

#Preset VNA
na.write(":SYST:PRES; *OPC?;")
opc=na.read()

#Set Frequencies, Number of Points, and IFBW
na.write("SENS:FREQ:STAR 10e6") #Set Start Freq
na.write("SENS:FREQ:STOP 9e9") #Set Stop Freq
na.write("SENS:SWE:POIN 1601") #Set Number of Points
na.write("SENS:BAND 1e3") #Set IFBW

#Set timeout to accomodate cal time (variable)
na.timeout = 90000 #set in milliseconds

#Run ecal between ports 1 and 2
na.write("SENS:CORR:COLL:GUID:ECAL:ACQ SOLR,1,2")
na.query("*OPC?") #Wait for calibration to complete...must read back the +1

print("Cal Complete")

drm.close()