pragma solidity ^0.8.0;

contract Exploit
{
    address target;
    constructor() {}
    function setup() public 
    {
        dummy dum = new dummy();
        target = address(dum);
    }
    function exploit() public
    {
        dummy(target).bad_transaction();
    }
}