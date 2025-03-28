import time
from pyfingerprint.pyfingerprint import PyFingerprint

# Initialize the fingerprint sensor with default baud rate
try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError('The given fingerprint sensor password is wrong!')
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

try:
    
    print('Currently stored templates: ' + str(f.getTemplateCount()))
    print('Currently used memory: ' + str(f.getStorageCapacity()))

    while True:
        try:
            print('Waiting for finger...')
            while not f.readImage():
                pass

            f.convertImage(0x01)
            result = f.searchTemplate()
            positionNumber = result[0]
            accuracyScore = result[1]


            if positionNumber == -1:
                print('No match found!')
            else:
                print('Found template at position #' + str(positionNumber))
                print('The accuracy score is: ' + str(accuracyScore))

            print('Remove finger...')
            time.sleep(2)
            time.sleep(0.1)  # Adding a short delay to stabilize communication

        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)

except Exception as e:
    print('Failed to set new baud rate!')
    print('Exception message: ' + str(e))
    exit(1)
