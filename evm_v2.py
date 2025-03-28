import time
from pyfingerprint.pyfingerprint import PyFingerprint
from RPLCD.i2c import CharLCD
from web3 import Web3
import RPi.GPIO as GPIO

# WEB3 setup
ganache_url = "http://192.168.0.205:7545" #replace with your rpc server's node url and port
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("Connected to Ganache")
else:
    print("Failed to connect to Ganache")
    exit(1)
    
    
contract_address = "0x9f258C52649D129a61856Ab5a16E1560b3667169"  #replace with your deployed contract address
abi = '''
[{
    "inputs": [{"internalType": "string", "name": "candidate", "type": "string"}],
    "name": "vote",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
},
{
    "inputs": [{"internalType": "address", "name": "voter", "type": "address"}],
    "name": "hasVoted",
    "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
    "stateMutability": "view",
    "type": "function"
}]
'''
contract = web3.eth.contract(address=contract_address, abi=abi)

# Logging into admin's local device
def log_vote(candidate, status, tx_hash=None, error=None):
    log_file_path = "log_vote.txt"
    with open(log_file_path, "a") as log_file:
        log_file.write(f"Vote for {candidate} - Status: {status}")
        if tx_hash:
            log_file.write(f", Transaction Hash: {tx_hash.hex()}")
        if error:
            log_file.write(f", Error registering vote in blockchain : {error}")
        log_file.write("\n")
        
# Initializing the fingerprint sensor // Change baud rate if your module is diff //mine: za620-m5 (8 pin)  
try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError('The given fingerprint sensor password is wrong!')
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

# Initializing LCD / Used ZHD 16*2 LCD module + i2c converter
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()

# gpio setup for buttons (using Broadcom gpio numering instead of physical num on the raspberry pi)
GPIO.setmode(GPIO.BCM)

# gpio pins for different candidates
PartyA_PIN = 17
PartyB_PIN = 27
PartyC_PIN = 22
CONFIRM_PIN = 24

# Setting up GPIO pins with pull-up resistors / using negative-logic to trigger
GPIO.setup(PartyA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(PartyB_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      
GPIO.setup(PartyC_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(CONFIRM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def detect_buttons():
    PartyA_vote = False
    PartyB_vote = False
    PartyC_vote = False
    confirm_vote = False

    while not confirm_vote:
        if GPIO.input(PartyA_PIN) == GPIO.LOW: 
            PartyA_vote = True
            print("PartyA Vote Selected")
            lcd.clear()
            lcd.write_string('PartyA Selected')
            time.sleep(0.5)

        if GPIO.input(PartyB_PIN) == GPIO.LOW:
            PartyB_vote = True
            print("PartyB Vote Selected")
            lcd.clear()
            lcd.write_string('PartyB Selected')
            time.sleep(0.5)

        if GPIO.input(PartyC_PIN) == GPIO.LOW:
            PartyC_vote = True
            print("PartyC Vote Selected")
            lcd.clear()
            lcd.write_string('PartyC Selected')
            time.sleep(0.5)

        if GPIO.input(CONFIRM_PIN) == GPIO.LOW:
            confirm_vote = True
            print("Vote Confirmed")
            lcd.clear()
            lcd.write_string('Vote Confirmed')
            time.sleep(0.5)

    return PartyA_vote, PartyB_vote, PartyC_vote


def get_eth_account_index_by_position(positionNumber):
    with open('voter_data.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            
            # Extracting the position number from the first part
            position = int(parts[0])
            
            if position == positionNumber:
                return position    
    return None

try:
    # optional but useful
    lcd.write_string('Regd Voters: ' + str(f.getTemplateCount()))
    time.sleep(2)
    lcd.clear()
    lcd.write_string('Blockchain EVM')
    time.sleep(2)
    lcd.clear()

    while True: 
        try:
            lcd.clear()
            lcd.write_string('Waiting for finger...')
            time.sleep(2)

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
                
                lcd.write_string(f'Authenticated! U#{positionNumber} Acc: {accuracyScore}')

                PartyA, PartyB, PartyC = detect_buttons()
                print("Level1")
                
                index = int(get_eth_account_index_by_position(positionNumber))
                web3.eth.default_account = web3.eth.accounts[index]  # Set default account for transactions, diff voters=diff account       
                voter_address = web3.eth.default_account   # Get the address of the voter  

                print("Level2")
                # Check if the voter has already voted
                has_voted = contract.functions.hasVoted(voter_address).call()
                if has_voted:
                    lcd.clear()
                    print("Level3")
                    lcd.write_string('Already voted!')
                    time.sleep(20)
                    continue

                if PartyA:
                    print("Sending vote for PartyA")
                    candidate = "PartyA"
                    try:
                        tx_hash = contract.functions.vote(candidate).transact({
                            'from': web3.eth.default_account,
                            'gas': 200000  
                        })
                        web3.eth.wait_for_transaction_receipt(tx_hash)
                        print(f"Transaction Hash: {tx_hash.hex()}")
                        log_vote(candidate, "Success", tx_hash=tx_hash)
                    except Exception as e:
                        print(f"Error during transaction: {str(e)}")
                        lcd.clear()
                        lcd.write_string('Vote Failed')
                        log_vote(candidate, "Failed", error=str(e))
                        time.sleep(2)

                if PartyB:
                    print("Sending vote for PartyB")
                    candidate = "PartyB"
                    try:
                        tx_hash = contract.functions.vote(candidate).transact({
                            'from': web3.eth.default_account,
                            'gas': 200000  
                        })
                        web3.eth.wait_for_transaction_receipt(tx_hash)
                        print(f"Transaction Hash: {tx_hash.hex()}")
                        log_vote(candidate, "Success", tx_hash=tx_hash)
                    except Exception as e:
                        print(f"Error during transaction: {str(e)}")
                        lcd.clear()
                        lcd.write_string('Vote Failed')
                        log_vote(candidate, "Failed", error=str(e))
                        time.sleep(2)

                if PartyC:
                    print("Sending vote for PartyC")
                    candidate = "PartyC"
                    try:
                        tx_hash = contract.functions.vote(candidate).transact({
                            'from': web3.eth.default_account,
                            'gas': 200000  
                        })
                        web3.eth.wait_for_transaction_receipt(tx_hash)
                        print(f"Transaction Hash: {tx_hash.hex()}")
                        log_vote(candidate, "Success", tx_hash=tx_hash)
                    except Exception as e:
                        print(f"Error during transaction: {str(e)}")
                        lcd.clear()
                        lcd.write_string('Vote Failed')
                        log_vote(candidate, "Failed", error=str(e))
                        time.sleep(2)

                # Resetting vote flags for the next round
                PartyA = PartyB = PartyC = False
                time.sleep(1)  

            # delay for user to remove finger
            time.sleep(2)
            lcd.clear()

        except Exception as e:
            if 'The image contains too few feature points' in str(e):
                print("Error: The image contains too few feature points")
                lcd.clear()
                lcd.write_string("Place Properly!")
                time.sleep(2)
                continue  
            

except Exception as e:
    lcd.clear()
    lcd.write_string('Unknown Error!')
    print('Unknown error, check ')
    print('Exception message: ' + str(e))
    exit(1)

finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit
    
