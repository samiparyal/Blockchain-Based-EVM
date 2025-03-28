// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    address public owner;
    mapping(string => uint256) public votes;  // Mapping to store the number of votes for each candidate
    mapping(address => bool) public hasVoted; // Mapping to track if an address has already voted

    // Constructor to set the contract deployer as the owner
    constructor() {
        owner = msg.sender;
    }

    // Function to vote for a candidate
    function vote(string memory candidate) public {
        require(!hasVoted[msg.sender], "You have already voted!");

        votes[candidate]++;

        hasVoted[msg.sender] = true;
    }

    // Function to get the total votes of a candidate
    function getVotes(string memory candidate) public view returns (uint256) {
        return votes[candidate];
    }
}