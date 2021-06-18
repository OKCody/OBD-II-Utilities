import obd

# Start connection to USB ELM 327 OBD-II device
conn = obd.OBD()

# Read and display codes in order to confirm that user wants to clear them
print('')
print('--- clear.py --------------------------------')
before = conn.query(obd.commands.GET_DTC)
print('CODES FOUND: ', before.value)

# Prompt user to confirm codes should be cleared
# If 'yes' clear codes then read codes again to confirm none remain, otherwise exit
print('---------------------------------------------')
i = input('Clear diagnostic trouble code(s)? (yes/no) ')
if i.upper() == 'YES':
    clear = conn.query(obd.commands.CLEAR_DTC)
    after = conn.query(obd.commands.GET_DTC)
    if not after:
        print('~~~ CODES CLEARED ~~~')
    else:
        print('~~~ ERROR: CODES NOT CLEARED ~~~')
        print('CODES REMAINING: ', after.value)
else:
    print('~~~ CODES NOT CLEARED ~~~')
print('---------------------------------------------')
print('')

# Close connection to USB ELM 327 ODB-II device
conn.close()
