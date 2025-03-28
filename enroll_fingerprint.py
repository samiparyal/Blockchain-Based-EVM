import time
from pyfingerprint.pyfingerprint import PyFingerprint
from RPLCD.i2c import CharLCD

index=0

# Initializing the fingerprint sensor // Change baud rate if your module is diff //mine: za620-m5 (8 pin)
try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError('The given fingerprint sensor password is wrong!')
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

# Initializing LCD / Used ZHD 16*2 LCD module
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()

def enroll_fingerprint():
    lcd.clear()
    lcd.write_string('Waiting for finger...')
    
    # Waiting for the finger to be read
    while not f.readImage():
        pass

    # Converting the read image to characteristics and store in charBuffer1
    f.convertImage(0x01)

    # Checking if the fingerprint is already stored
    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber >= 0:
        lcd.clear()
        lcd.write_string(f'Fingerprint\nexists at pos {positionNumber}.')
        time.sleep(2)
        return positionNumber
    

    lcd.clear()
    lcd.write_string('Remove finger...')
    time.sleep(2)

    lcd.clear()
    lcd.write_string('Waiting for same finger...')
    
    while not f.readImage():
        pass

    # Convert the read image to characteristics and store in charBuffer2
    f.convertImage(0x02)

    # Comparing (both) the characteristics 
    if f.compareCharacteristics() == 0:
        lcd.clear()
        lcd.write_string('Fingers do not match!')
        time.sleep(2)
        raise Exception('Fingers do not match.')

    # Creating a template
    f.createTemplate()

    # Storing the template and echo the position number
    positionNumber = f.storeTemplate()
    lcd.clear()
    lcd.write_string(f'Fingerprint\nstored at pos {positionNumber}.')
    time.sleep(2)

    return positionNumber

try:
    new_user_position = enroll_fingerprint()
    print(f'New user fingerprint enrolled at position {new_user_position}.')
    
    lcd.clear()
    lcd.write_string('Enter voter name:')
    time.sleep(2)
    
    # Here, you can store any relevant/necessary info like Citizenship no, NID or else. For instance, i am storing Voter's Name only
    voter_name = input('Enter voter name: ')

    with open('voter_data.txt', 'a') as file:
        file.write(f'{new_user_position},{voter_name},{index}\n')
        index+=1
    print('Voter data saved.')

    lcd.clear()
    lcd.write_string('Voter data saved.')
    time.sleep(2)
    
except Exception as e:
    print(f'An error occurred during enrollment: {str(e)}')
    lcd.clear()
    lcd.write_string('Try Again!')
    time.sleep(2)
