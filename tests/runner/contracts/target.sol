pragma solidity ^0.8.0;

contract dummy
{
    mapping (address => uint256) balances;
    address owner;
    constructor() 
    {
        owner = msg.sender;
    }
    function set_balance(address reciever, uint256 balance) external
    {
        balances[reciever] = balance;
    }
    function fuck_off() external
    {
        require(msg.sender != owner, "screw you");
    }
    function bad_transaction() external
    {
        payable(msg.sender).transfer(balances[msg.sender]+100);
    }
}