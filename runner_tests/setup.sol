pragma solidity ^0.4.23;

import "./target.sol";

contract Deployer {
    function setup() public returns (address) {
        TestContract testContract = new TestContract();
        return address(testContract);
    }
}