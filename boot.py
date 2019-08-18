# This file is executed on every boot (including wake-boot from deepsleep)

# import esp
# esp.osdebug(None)

print('start boot.py execution')

# activate webrepl
import webrepl

webrepl.start()

print('end boot.py execution')
