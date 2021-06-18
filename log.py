import obd
import time
import datetime

# Start connection to USB ELM 327 OBD-II device in asynchronous mode
# Asynchronous mode polls watched parameters and stores their latest values.
# when queried, the latest value is returned
conn = obd.Async()

# A list of all the commands built into the Python OBD library. Not all vehicles
# support all commands
cmds=['PIDS_A','STATUS','FREEZE_DTC','FUEL_STATUS','ENGINE_LOAD','COOLANT_TEMP','SHORT_FUEL_TRIM_1','LONG_FUEL_TRIM_1','SHORT_FUEL_TRIM_2','LONG_FUEL_TRIM_2','FUEL_PRESSURE','INTAKE_PRESSURE','RPM','SPEED','TIMING_ADVANCE','INTAKE_TEMP','MAF','THROTTLE_POS','AIR_STATUS','O2_SENSORS','O2_B1S1','O2_B1S2','O2_B1S3','O2_B1S4','O2_B2S1','O2_B2S2','O2_B2S3','O2_B2S4','OBD_COMPLIANCE','O2_SENSORS_ALT','AUX_INPUT_STATUS','RUN_TIME','PIDS_B','DISTANCE_W_MIL','FUEL_RAIL_PRESSURE_VAC','FUEL_RAIL_PRESSURE_DIRECT','O2_S1_WR_VOLTAGE','O2_S2_WR_VOLTAGE','O2_S3_WR_VOLTAGE','O2_S4_WR_VOLTAGE','O2_S5_WR_VOLTAGE','O2_S6_WR_VOLTAGE','O2_S7_WR_VOLTAGE','O2_S8_WR_VOLTAGE','COMMANDED_EGR','EGR_ERROR','EVAPORATIVE_PURGE','FUEL_LEVEL','WARMUPS_SINCE_DTC_CLEAR','DISTANCE_SINCE_DTC_CLEAR','EVAP_VAPOR_PRESSURE','BAROMETRIC_PRESSURE','O2_S1_WR_CURRENT','O2_S2_WR_CURRENT','O2_S3_WR_CURRENT','O2_S4_WR_CURRENT','O2_S5_WR_CURRENT','O2_S6_WR_CURRENT','O2_S7_WR_CURRENT','O2_S8_WR_CURRENT','CATALYST_TEMP_B1S1','CATALYST_TEMP_B2S1','CATALYST_TEMP_B1S2','CATALYST_TEMP_B2S2','PIDS_C','STATUS_DRIVE_CYCLE','CONTROL_MODULE_VOLTAGE','ABSOLUTE_LOAD','COMMANDED_EQUIV_RATIO','RELATIVE_THROTTLE_POS','AMBIANT_AIR_TEMP','THROTTLE_POS_B','THROTTLE_POS_C','ACCELERATOR_POS_D','ACCELERATOR_POS_E','ACCELERATOR_POS_F','THROTTLE_ACTUATOR','RUN_TIME_MIL','TIME_SINCE_DTC_CLEARED','MAX_MAF','FUEL_TYPE','ETHANOL_PERCENT','EVAP_VAPOR_PRESSURE_ABS','EVAP_VAPOR_PRESSURE_ALT','SHORT_O2_TRIM_B1','LONG_O2_TRIM_B1','SHORT_O2_TRIM_B2','LONG_O2_TRIM_B2','FUEL_RAIL_PRESSURE_ABS','RELATIVE_ACCEL_POS','HYBRID_BATTERY_REMAINING','OIL_TEMP','FUEL_INJECT_TIMING','FUEL_RATE']

# Build a list of commands, via trial and error, supported by the connected
# vehicle.
supported = []
for each in cmds:
    if conn.supports(obd.commands[each]):
        supported += [each]

# Watch all supported parameters
for each in supported:
    conn.watch(obd.commands[each])

# Begin polling supported parameters
conn.start()

# Allow enough time for all supported values to be initialized
time.sleep(5)

# Determine which supported commands return scalar values.
# Some supported parameters do not return nuneric values. I'm only interested in
# numeric data at the moment. Other value types could be supported later . . .
scalars = []
header = []
for each in supported:
    r = conn.query(obd.commands[each])
    if type(r.value).__name__ == 'Quantity':
        scalars += [each]
        header += [each + ' (' + r.unit + ')']

# Print header with 'TIME (UTC)' prepended as time will be supplied by the
# machine running this script, not the OBD-II device
header = ['TIME (UTC)'] + header
print(*header, sep=',')

# Until this script is interrupted, query each supported parameter that returns
# a numeric value and print the results as a comma separated string to standard
# output such that it can be read directly or redirected to a file from the
# terminal - not a robust method of timestamping ro writing data do disk, but
# should work well enough for shade tree mechanics. Sample rate of twice per
# second was determined experimentally. Fewer samples might be just as useful
# in some cases.  More samples might not be possible. -mileage may vary . . .
while True:
    line = []
    line += [str(datetime.datetime.utcnow())]
    for each in scalars:
        r = conn.query(obd.commands[each])
        line += [r.value.magnitude]
    print(*line, sep=',')
    time.sleep(.5)

# Close connection to USB ELM 327 ODB-II device
conn.close()
