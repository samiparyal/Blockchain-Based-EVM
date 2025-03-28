# Blockchain-Based-EVM
This is my 3rd year (EEE) engineering project. It introduces a novel approach to electronic voting systems by integrating blockchain technology to enhance security and transparency. The primary objective is to address the ongoing challenges faced by traditional voting systems. The project focuses on designing and implementing an electronic voting system that incorporates secured cryptographic mechanisms, comprising an EVM and an IoT-based decentralized consensus mechanism to facilitate secure and tamper-proof voting. The process involves creating and cross-referencing hashed fingerprint data for user authentication, encrypting the voting information, and sending it to the Ethereum blockchain in real-time. Blockchain protocols are incorporated to guarantee the security and unchangeability of votes. The primary demonstration of the project is the system's ability to provide secure and tamper-proof voting, allowing voters to verify vote integrity while preserving anonymity. Through blockchain's decentralized architecture, the system minimizes the risk of central points of failure and enhances resilience against hacking, tampering, and other cyber-attacks. The project's main conclusion is that blockchain-based electronic voting systems offer a practical, secure and effective solution for modernizing electoral processes while upholding democratic integrity, representing a significant technological advancement in democratic governance.  

## How To Run this?
1. Get a Raspberry Pi
    --> A Raspberry Pi (preferably 3 or 4) is recommended.
    --> You can use other microcontrollers, but they must support Python, GPIO, and Web3 interaction (via web3.py).

3. Download this entire repository
    --> Clone or download the project files to your Raspberry Pi:
      ```
       git clone https://github.com/samiparyal/Blockchain-Based-EVM
       cd <project-folder>
      ```
4. Connect the Hardware
    --> LCD Display with I2C module (I've use ZHD 16*2 module)
    --> Any Fingerprint Sensor via UART TX/RX (recommended: 8 pin za650_m5)
    --> 3 Buttons (for voting) + 1 Confirm Button (you can custom your configuration as needed)
    --> Add pull-up or pull-down resistors based on your GPIO setup (Modify the code's GPIO logic if you're changing resistor config)

5. Start Ganache
    --> Open Ganache on your computer
    --> Create a new workspace
    --> Keep your HTTP RPC URL to 'All Interfaces' for easy use 

6. Compile the Smart Contract with Truffle
    --> Make sure you're in your project folder
    --> Compile the contract:
        ```
          truffle compile
       ```
   
8. Deploy the Contract to Ganache
      ```
          truffle migrate --reset
      ```
9. Copy the new contract address from the output
10. Update it in:
    --> evm_v2.py (Python backend script)
    --> app.js (JavaScript frontend)

11. Test the Python Voting System:
    --> Configure Pi Os on your raspberry first
    --> Open your Raspberry environment on Putty or RealVNC
    --> Activate your virtual environment:
    ```
        source myenv/bin/activate
    ```
12. Run the script:
    ```
        python3 evm_v2.py
    ```
13. Try authenticating a finger and casting a vote (Make sure to enroll voters using enroll_fingerprint.py beforehand)
14. View Results in the Browser by opening UI.Html
