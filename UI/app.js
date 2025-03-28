console.log("app.js loaded!");
const web3 = new Web3('http://192.168.0.105:7545'); 

//contract and abi
const contractAddress = "0x9f258C52649D129a61856Ab5a16E1560b3667169"; 
const abi = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "candidate",
                "type": "string"
            }
        ],
        "name": "vote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "voter",
                "type": "address"
            }
        ],
        "name": "hasVoted",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "candidate",
                "type": "string"
            }
        ],
        "name": "getVotes",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
];

const contract = new web3.eth.Contract(abi, contractAddress);

async function getVoteCounts() {
    try {
        // Fetching vote counts from the smart contract for each candidate
        const PartyAVotes = await contract.methods.getVotes('PartyA').call();
        const PartyBVotes = await contract.methods.getVotes('PartyB').call();
        const PartyCVotes = await contract.methods.getVotes('PartyC').call();

        // Updating the vote counts in the HTML
        document.getElementById('voteCountPartyA').innerText = PartyAVotes || '0';
        document.getElementById('voteCountPartyB').innerText = PartyBVotes || '0';
        document.getElementById('voteCountPartyC').innerText = PartyCVotes || '0';
        
    } catch (error) {
        console.error("Error fetching vote counts:", error);
        document.getElementById('voteCountPartyA').innerText = 'Error';
        document.getElementById('voteCountPartyB').innerText = 'Error';
        document.getElementById('voteCountPartyC').innerText = 'Error';
    }
}

// Calling the function to fetch the vote counts
getVoteCounts();
