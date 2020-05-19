import visa
import time
# start of PNA_Integrated_Pulse_Narrowband_Setup

# This example sets up a narrowband pulsed configuration using the integrated pulse measurement option (N52xxA #008 or S93026A/B).  The process defines a 500ns pulse with a 10% duty cycle that is transmitted from port 1 to port 2 of the VNA.  It then completes a guided 2 port calibration (unpulsed) with power and then switches to a couple power sweeps at different frequencies and then recalls the base state again.  The program uses the non-default pulse generators 3 and 4 to control the gate and modulator drives in order to show the process for using the non-default settings.

rm = visa.ResourceManager()
PNA_X = rm.open_resource('TCPIP0::141.121.210.126::hislip0::INSTR')
PNA_X.timeout = 10000
# Preset PNA and wait for completion
PNA_X.write(':SYSTem:PRESet')
temp_values = PNA_X.query_ascii_values('*OPC?')
opc = int(temp_values[0])

PNA_X.write(':CALCulate:PARameter:DELete:ALL')
# Setup Measurements that are desired (S21, S12)
PNA_X.write(':CALCulate:PARameter:DEFine:EXTended "%s","%s"' % ('MyS21', 'S21'))
PNA_X.write(':CALCulate:PARameter:DEFine:EXTended "%s","%s"' % ('MyS12', 'S12'))
PNA_X.write(':CALCulate:PARameter:DEFine:EXTended "%s","%s"' % ('MyB', 'B,1'))
PNA_X.write(':CALCulate:PARameter:DEFine:EXTended "%s","%s"' % ('MyR1', 'R1,1'))
PNA_X.write(':DISPlay:WINDow1:TRACe1:FEED "%s"' % ('MyS21'))
PNA_X.write(':DISPlay:WINDow1:TRACe2:FEED "%s"' % ('MyS12'))
PNA_X.write(':DISPlay:WINDow1:TRACe3:FEED "%s"' % ('MyB'))
PNA_X.write(':DISPlay:WINDow1:TRACe4:FEED "%s"' % ('MyR1'))
# Setup Sweep Frequency and Number of Points
PNA_X.write(':SENSe:FREQuency:STARt %G GHZ' % (1.85))
PNA_X.write(':SENSe:FREQuency:STOP %G GHZ' % (5.55))
PNA_X.write(':SENSe:SWEep:POINts %d' % (9))
# Set PRF to Fixed Mode
PNA_X.write(':SENSe:SWEep:PULSe:PRF:AUTO %d' % (0))
# Set to Standard Pulsed mode and set PW (500 ns) and Period (5 us)
PNA_X.write(':SENSe:SWEep:PULSe:MASTer:WIDTh %G' % (5e-07))
PNA_X.write(':SENSe:SWEep:PULSe:MASTer:PERiod %G' % (5e-06))
PNA_X.write(':SENSe:SWEep:PULSe:MODE %s' % ('STD'))
# Disable Auto IFBW and Set IFBW (10 Hz)
PNA_X.write(':SENSe:SWEep:PULSe:IFBW:AUTO %d' % (0))
PNA_X.write(':SENSe:BANDwidth:RESolution %G' % (10.0))
# Disable Auto Pulse Detect Mode and set mode to Narrowband
PNA_X.write(':SENSe:SWEep:PULSe:DETectmode:AUTO %d' % (0))
PNA_X.write(':SENSe:SWEep:PULSe:WIDeband:STATe %d' % (0))
# Set Auto Timing of pulse width and delays
PNA_X.write(':SENSe:SWEep:PULSe:TIMing:AUTO %d' % (1))
PNA_X.write(':SENSe:SWEep:PULSe:DRIVe:AUTO %d' % (0))
# Get Calculated Default Modulator Drive Info
mod_width = float(PNA_X.query(':SENSe:PULSe1:WIDTh?'))
mod_period = float(PNA_X.query(':SENSe:PULSe1:PERiod?'))
mod_delay = float(PNA_X.query(':SENSe:PULSe1:DELay?'))
# Get Calculated Default Gate Drive Info
gate_width = float(PNA_X.query(':SENSe:PULSe2:WIDTh?'))
gate_period = float(PNA_X.query(':SENSe:PULSe2:PERiod?'))
gate_delay = float(PNA_X.query(':SENSe:PULSe2:DELay?'))

# Setup which pulse gen is for modulation source (Pulse 4) and for IF gates (Pulse 3).
PNA_X.write(':SENSe:PATH:CONFig:ELEMent:STATe "%s","%s"' % ('Src1Out1PulseModEnable', 'Enable'))
PNA_X.write(':SENSe:PATH:CONFig:ELEMent:STATe "%s","%s"' % ('PulseModDrive', 'Pulse4'))
PNA_X.write(':SENSe:PATH:CONFig:ELEMent:STATe "%s","%s"' % ('IFGateA', 'Pulse3'))
PNA_X.write(':SENSe:PATH:CONFig:ELEMent:STATe "%s","%s"' % ('IFGateB', 'Pulse3'))
PNA_X.write(':SENSe:PATH:CONFig:ELEMent:STATe "%s","%s"' % ('IFGateR1', 'Pulse3'))
PNA_X.write(':SENSe:PATH:CONFig:ELEMent:STATe "%s","%s"' % ('IFGateR2', 'Pulse3'))
# Setup Pulse Generators that are being used
PNA_X.write(':SENSe:PULSe4:WIDTh %G' % (mod_width))
PNA_X.write(':SENSe:PULSe3:WIDTh %G' % (gate_width))
PNA_X.write(':SENSe:PULSe4:PERiod %G' % (mod_period))
PNA_X.write(':SENSe:PULSe3:PERiod %G' % (gate_period))
PNA_X.write(':SENSe:PULSe4:DELay %G' % (mod_delay))
PNA_X.write(':SENSe:PULSe3:DELay %G' % (gate_delay))
PNA_X.write(':SENSe:PULSe1:STATe %d' % (0))
PNA_X.write(':SENSe:PULSe2:STATe %d' % (0))
PNA_X.write(':SENSe:PULSe3:STATe %d' % (1))
PNA_X.write(':SENSe:PULSe4:STATe %d' % (1))
# Turn off pulsing to calibrate (optional)
PNA_X.write(':SENSe:PATH:CONFig:ELEMent:STATe "%s","%s"' % ('Src1Out1PulseModEnable', 'Disable'))
# Set port connectors and cal kits
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:CONNector:PORT1:SELect "%s"' % ('1.85 mm female'))
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:CONNector:PORT2:SELect "%s"' % ('1.85 mm male'))
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:CONNector:PORT3:SELect "%s"' % ('Not used'))
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:CONNector:PORT4:SELect "%s"' % ('Not used'))
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:CKIT:PORT1:SELect "%s"' % ('N4694D ECal MY59410162'))
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:CKIT:PORT2:SELect "%s"' % ('N4694D ECal MY59410162'))
# Enable Power Calibration on Port 1
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:PSENsor1:STATe %d' % (1))
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:PSENsor1:CONNector "%s"' % ('Ignored'))
# Set Power Level for Power Calibration step of calibration
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:PSENsor1:POWer:LEVel %G' % (-10.0))
# Set cal thru method to analyzer default
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:METHod %s' % ('DEFAULT'))
# Determine the steps needed to complete the calibration
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:INITiate:IMMediate')
temp_values = PNA_X.query_ascii_values(':SENSe:CORRection:COLLect:GUIDed:STEPs?')
steps = int(temp_values[0])

PNA_X.timeout = 90000
# Measure Cal Standards
data = PNA_X.query(':SENSe:CORRection:COLLect:GUIDed:DESCription? %d' % (1))
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:ACQuire %s' % ('STAN1'))
temp_values = PNA_X.query_ascii_values('*OPC?')
opc1 = int(temp_values[0])

data1 = PNA_X.query(':SENSe:CORRection:COLLect:GUIDed:DESCription? %d' % (2))
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:ACQuire %s' % ('STAN2'))
temp_values = PNA_X.query_ascii_values('*OPC?')
opc2 = int(temp_values[0])

PNA_X.timeout = 10000
PNA_X.write(':SENSe:CORRection:COLLect:GUIDed:SAVE:IMMediate')
# Re-enable pulsing
PNA_X.write(':SENSe:PATH:CONFig:ELEMent:STATe "%s","%s"' % ('Src1Out1PulseModEnable', 'Enable'))
PNA_X.write(':MMEMory:STORe:FILE "%s"' % ('test.csa'))
temp_values = PNA_X.query_ascii_values('*OPC?')
opc3 = int(temp_values[0])

PNA_X.write(':MMEMory:LOAD:FILE "%s"' % ('test.csa'))
temp_values = PNA_X.query_ascii_values('*OPC?')
opc4 = int(temp_values[0])

# Change to a Single Frequency Power Sweep
PNA_X.write(':SOURce:POWer1:STARt %G' % (-35.0))
PNA_X.write(':SOURce:POWer1:STOP %G' % (-5.0))
PNA_X.write(':SENSe:SWEep:TYPE %s' % ('POWer'))
PNA_X.write(':SENSe:FREQuency:CW %G GHZ' % (2.0))
time.sleep(10)
# Change CW frequency to 3 GHz
PNA_X.write(':SENSe:FREQuency:CW %G GHZ' % (3.0))
time.sleep(10)
# Reload original state file
PNA_X.write(':MMEMory:LOAD:FILE "%s"' % ('test.csa'))
temp_values = PNA_X.query_ascii_values('*OPC?')
opc5 = int(temp_values[0])

PNA_X.close()
rm.close()

# end of PNA_Integrated_Pulse_Narrowband_Setup
