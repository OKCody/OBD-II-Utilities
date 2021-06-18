import obd

# Start connection to USB ELM 327 OBD-II device
conn = obd.OBD()

# Read and display diagnostic trouble codes
print('')
print('--- codes.py --------------------------------')
r = conn.query(obd.commands.GET_DTC)
print('GET_DTC: ', r.value)

# Read and display freeze frame data if it exists
print('---------------------------------------------')
r = conn.query(obd.commands.FREEZE_DTC)
print('FREEZE_DTC: ', r.value)

# Read and display fuel system status if it exists. open loop, closed loop, etc.
print('---------------------------------------------')
r = conn.query(obd.commands.FUEL_STATUS)
print('FUEL_STATUS: ', r.value)

# Read and display air system status if it exists
print('---------------------------------------------')
r = conn.query(obd.commands.AIR_STATUS)
print('AIR_STATUS: ', r.value)

# Read and dispaly O2 sensor status if it exists
print('---------------------------------------------')
r = conn.query(obd.commands.O2_SENSORS)
print('O2_SENSORS: ', r.value)

# Close connection to USB ELM 327 ODB-II device
conn.close()


# https://www.youtube.com/watch?v=7gdZ2o6osAI

# P2188 is the code that's causing the check engine light
