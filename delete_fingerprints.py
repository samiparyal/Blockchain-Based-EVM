import time
from pyfingerprint.pyfingerprint import PyFingerprint

# Initializing the fingerprint sensor // Change baud rate if your module is diff
try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError('The given fingerprint sensor password is wrong!')
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

def delete_all_fingerprints():
    try:
        # just checking storage cap
        storage_capacity = f.getStorageCapacity()
        print('Deleting all fingerprints...')
        
        for i in range(storage_capacity):
            if f.deleteTemplate(i):
                print(f'Successfully deleted fingerprint at position {i}.')
            else:
                print(f'Failed to delete fingerprint at position {i} or no fingerprint at this position.')

        print('All fingerprints have been deleted.')
    except Exception as e:
        print(f'An error occurred while deleting fingerprints: {str(e)}')
        
delete_all_fingerprints()
