// SPDX-License-Identifier: MIT

pragma solidity ^0.8.17;

import "console.sol";

contract PoW {
    uint8 public parent_difficulty;
    address public owner;

    constructor() {
        owner = msg.sender;
        parent_difficulty = 238;
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
