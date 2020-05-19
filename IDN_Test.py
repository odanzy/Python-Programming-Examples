import visa

drm = visa.ResourceManager()

vi = drm.open_resource("TCPIP0::localhost::hislip0::INSTR")

print(vi.query("*IDN?").strip())

drm.close()