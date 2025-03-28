import time
from pyfingerprint.pyfingerprint import PyFingerprint
from RPLCD.i2c import CharLCD

try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError('The given fingerprint sensor password is wrong!')
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()

try:
    lcd.write_string('Templates: ' + str(f.getTemplateCount()))
    time.sleep(2)
    lcd.clear()
    lcd.write_string('Memory Used: ' + str(f.getStorageCapacity()))
    time.sleep(2)
    lcd.clear()

    while True:
        try:
            lcd.write_string('Waiting for finger...')
            time.sleep(2)
            lcd.clear()

            while not f.readImage():
                pass

            f.convertImage(0x01)
            result = f.searchTemplate()
            positionNumber = result[0]
            accuracyScore = result[1]

            lcd.clear()
            if positionNumber == -1:
                lcd.write_string('No match found!')
            else:
                lcd.write_string(f'Found at pos #{positionNumber}')
                lcd.crlf()
                lcd.write_string(f'Acc: {accuracyScore}')

            time.sleep(2)
            lcd.clear()

        except Exception as e:
            lcd.clear()
            lcd.write_string('Operation failed!')
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)

except Exception as e:
    lcd.clear()
    lcd.write_string('Failed to set baud rate!')
    print('Failed to set new baud rate!')
    print('Exception message: ' + str(e))
    exit(1)
