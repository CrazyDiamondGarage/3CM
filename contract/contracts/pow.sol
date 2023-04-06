// SPDX-License-Identifier: MIT

pragma solidity ^0.8.18;

import "./console.sol";


struct PoWCanidate {
    bytes32 commitment;
    address miner;
    uint64 nonce;
    PoWVote[] votes;
}

struct PoWVote {
    address miner;
    uint64 nonce;
}

struct UserAction {
    address user;
    bytes32 name;
    address value;
    uint32 nonce;
    bytes sig;
}

contract PoW {
    bytes32 public parent_hash;
    uint32 public parent_height;
    uint64 public parent_nonce;
    uint8 public parent_difficulty;
    uint public prev_timestamp;
    uint public gap_timestamp;

    // address public owner;
    uint public block_height;
    PoWCanidate[] public canidates;

    event NewBlock(address miner, uint height);

    constructor() {
        // owner = msg.sender;
        parent_difficulty = 238;
        parent_height = 0;
        // prev_timestamp = block.timestamp;
        prev_timestamp = 0;
        gap_timestamp = 10;
    }

    function new_block(bytes32 commitment, address miner, uint64 nonce, UserAction[] memory updates) external returns (bytes32) {
        require(block.timestamp >= prev_timestamp + gap_timestamp, "too early");
        PoWCanidate memory canidate;
        for (uint i = 0; i < canidates.length; i++) {
            canidate = canidates[i];
        }

        console.logBytes32(canidate.commitment);
        // require(parent_height + 1 == mining.block_height, "try add_block");
        bytes32 block_hash = sha256(bytes.concat(parent_hash, commitment, bytes4(parent_height+1), bytes20(miner), bytes8(nonce)));
        // console.logBytes32(parent_hash);
        // console.logUint(uint256(block_hash));
        // console.logUint(2**parent_difficulty);
        console.logUint(block.timestamp);
        console.logUint(prev_timestamp);
        console.logUint(gap_timestamp);
        // console.logBool(uint256(block_hash) < 2**parent_difficulty);
        require(uint256(block_hash) < 2**parent_difficulty, "difficulty required");

        parent_hash = block_hash;
        parent_nonce = nonce;
        parent_height = parent_height+1;
        prev_timestamp = block.timestamp;
        return block_hash;
    }

    function add_block(bytes32 commitment, address miner, uint64 nonce, UserAction[] memory updates) external returns (bytes32) {
        require(parent_height > 0, "try new_block");
        // require(nonce < parent_nonce, "lucky nonce required");
        // require(parent_height == mining.block_height, "try new_block");
        bytes32 block_hash = sha256(bytes.concat(parent_hash, bytes4(parent_height), bytes20(miner), bytes8(nonce)));
        require(uint256(block_hash) < 2**parent_difficulty, "difficulty required");

        parent_hash = block_hash;
        parent_nonce = nonce;
        return block_hash;
    }

    function get_number() public view returns (uint) {
        return block.number;
    }

    function get_timestamp() public view returns (uint) {
        return block.timestamp;
    }

    function get_difficulty(uint8 d) public view returns (uint256) {
        return 2**d;
    }
}
