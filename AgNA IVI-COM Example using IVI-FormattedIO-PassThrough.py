""" This is an example to show how to communicate using the IVI-COM driver for the analyzer.  The user needs to have comtypes installed prior to running this example. """

import comtypes.client as cc

na = cc.CreateObject("AgNA.AgNA")

#Connect to PNA over LAN
na.Initialize("TCPIP0::localhost::hislip10::INSTR", 0, 0, "")
#Connect using PXI Address
#na.Initialize("PXI0::", 0, 0, "")

# Get equivalent information from ID String using IVI Driver Properties
print('IVI Driver - Connected Model #: ' + na.Identity.InstrumentManufacturer + ',' + na.Identity.InstrumentModel + ',' + na.System.SerialNumber +',' + na.Identity.InstrumentFirmwareRevision)

## Access standard VISA COM Formatted IO interface 
vi = na.System.IO

### Ask for ID String 
vi.WriteString('*IDN?')
print('VISA-COM Formatted IO - Connected to: ' + vi.ReadString().strip())

## Access SCPI Interface through VISA Passthrough in instrument software
pt = na.System.ScpiPassThrough

### Ask for ID String
pt.WriteString('*IDN?')
print('VNA SCPI Passthrough - Connected to: ' + pt.ReadString())

na.Close()


