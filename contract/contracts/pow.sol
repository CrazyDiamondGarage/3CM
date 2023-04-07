// SPDX-License-Identifier: MIT

pragma solidity ^0.8.18;

import "./console.sol";


struct PoWCanidate {
    // bytes32 commitment;
    address miner;
    uint64 nonce;
    uint16 votes;
}

struct PoWVote {
    bytes32 commitment;
    // address miner;
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
    // uint64 public parent_nonce;
    uint8 public parent_difficulty;
    uint public prev_timestamp;
    uint public gap_seconds;

    uint public block_height;
    // PoWCanidate[] public canidates;

    uint public miner_count;
    mapping(uint => address) public miners;
    mapping(address => PoWVote) public votes;
    mapping(bytes32 => PoWCanidate) public canidates;

    event NewBlock(bytes32 indexed, address indexed, uint256 indexed);

    constructor() {
        // owner = msg.sender;
        parent_difficulty = 238;
        parent_height = 1;
        // prev_timestamp = block.timestamp;
        prev_timestamp = 0;
        gap_seconds = 0;
    }

    function new_block(bytes32 commitment, uint64 nonce, UserAction[] memory updates) external returns (bytes32) {
        address miner = msg.sender;
        require(block.timestamp >= prev_timestamp + gap_seconds, "too early");
        uint16 prev_votes = 0;
        PoWCanidate memory best_canidate;
        PoWVote memory best_vote;
        bool best = false;
        for (uint i = 0; i < miner_count; i++) {
                console.logUint(i);
            address m = miners[i];
            PoWVote memory v = votes[m];
            PoWCanidate memory c = canidates[v.commitment];
            if(c.votes > prev_votes){
                best_canidate = c;
                best_vote = v;
                best = true;
                prev_votes = c.votes;
                console.logUint(i);
            }
            delete miners[i];
            delete votes[m];
            delete canidates[v.commitment];
        }
        console.logBytes32(parent_hash);
        console.logBytes32(best_vote.commitment);
        console.logBytes20(bytes20(best_canidate.miner));
        console.logUint(parent_height);
        console.logUint(best_vote.nonce);
        if(best){
            parent_hash = sha256(bytes.concat(parent_hash, best_vote.commitment, bytes4(parent_height), bytes20(best_canidate.miner), bytes8(best_vote.nonce)));
            parent_height += 1;
        }
        // console.logBytes32(c.commitment);
        console.logUint(parent_height);
        console.logBytes32(parent_hash);

        // require(parent_height + 1 == mining.block_height, "try add_block");
        bytes32 block_hash = sha256(bytes.concat(parent_hash, commitment, bytes4(parent_height), bytes20(miner), bytes8(nonce)));
        // console.logUint(uint256(block_hash));
        // console.logUint(2**parent_difficulty);
        console.logUint(block.timestamp);
        console.logUint(prev_timestamp);
        console.logUint(gap_seconds);
        // console.logBool(uint256(block_hash) < 2**parent_difficulty);
        require(uint256(block_hash) < 2**parent_difficulty, "difficulty required");

        miner_count = 1;
        miners[0] = miner;
        votes[miner] = PoWVote(commitment, nonce);
        canidates[commitment] = PoWCanidate(miner, nonce, 1);
        // parent_nonce = nonce;
        prev_timestamp = block.timestamp;

        emit NewBlock(commitment, miner, parent_height+1);
        return block_hash;
    }

    function add_block(bytes32 commitment, uint64 nonce, UserAction[] memory updates) external returns (bytes32) {
        address miner = msg.sender;
        // require(parent_height > 0, "try new_block");
        // require(nonce < parent_nonce, "lucky nonce required");
        // require(parent_height == mining.block_height, "try new_block");
        console.logUint(parent_height);
        console.logBytes32(parent_hash);

        bytes32 block_hash = sha256(bytes.concat(parent_hash, commitment, bytes4(parent_height), bytes20(miner), bytes8(nonce)));
        require(uint256(block_hash) < 2**parent_difficulty, "difficulty required");

        // miner_count += 1;
        // miners[miner_count] = miner;
        // votes[miner] = PoWVote(commitment, nonce);
        // canidates[commitment] = PoWCanidate(miner, nonce, 1);
        // parent_hash = block_hash;
        // parent_nonce = nonce;
        emit NewBlock(commitment, miner, parent_height+1);
        return block_hash;
    }
}
