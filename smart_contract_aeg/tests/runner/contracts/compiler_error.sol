pragma solidity ^0.8.0;

contract Exploit
{
    constructor() 
    {}
    address target;
    function setup() public
    {
        dummy dum = new dummy();
        target = address(dum);
    }
    function exploit() public
    {
        dummy(target).baudrillard();
    }
}